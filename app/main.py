from fastapi import FastAPI
from .db import engine, Base
from .routes.auth import router as auth_router
from .routes.users import router as users_router
from .routes.ai import router as ai_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ai_router)



@app.get("/")
def read_root():
    return {"message": "AI SaaS Backend is running 🚀"}
