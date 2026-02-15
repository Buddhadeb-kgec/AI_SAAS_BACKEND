from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi import Query
from fastapi import HTTPException

from ..deps import get_db
from ..deps_auth import get_current_user
from ..models import AIResult, User
from ..services.ai_service import analyze_text
from ..schemas_ai import AIResultOut

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Read uploaded file
        content = await file.read()

        # Decode safely to text
        text = content.decode("utf-8", errors="ignore")

        # 🔥 Remove NULL characters that break PostgreSQL
        text = text.replace("\x00", "")

        # If file had no readable text
        if not text.strip():
            text = "Uploaded file contained non-text or binary content."

        # Call AI (mock or real)
        ai_output = analyze_text(text)

        # Save to database
        result = AIResult(
            content=text,
            ai_output=ai_output,
            user_id=current_user.id,
        )

        db.add(result)
        db.commit()
        db.refresh(result)

        return {"ai_output": ai_output}

    except Exception as e:
        # Prevent server crash and show clean error
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

@router.get("/history", response_model=List[AIResultOut])
def get_history(
    limit: int = Query(10, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(AIResult)
        .filter(AIResult.user_id == current_user.id)
        .order_by(AIResult.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return results

@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = (
        db.query(AIResult)
        .filter(AIResult.id == result_id, AIResult.user_id == current_user.id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    db.delete(result)
    db.commit()

    return {"message": "Result deleted successfully"}