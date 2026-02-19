from dotenv import load_dotenv
import os
from pathlib import Path
from openai import OpenAI

# 🔥 Force load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_text(text: str) -> str:
    """
    Analyze resume/document text using OpenAI.
    Returns structured ATS-style feedback.
    """

    # 🚫 No readable text
    if not text or not text.strip():
        return "No readable text found in the uploaded file."

    try:
        # 🔎 DEBUG: show what backend is actually sending to AI
        print("\n===== TEXT SENT TO AI (first 800 chars) =====\n")
        print(text[:800])
        print("\n=============================================\n")

        # 🧠 Strong ATS evaluation prompt
        prompt = f"""
You are a strict ATS (Applicant Tracking System) resume evaluator and professional career coach.

Carefully read the ENTIRE resume/document content and provide a **document-specific** evaluation.

Return your answer in this exact structured format:

Resume Score: <number out of 100>

ATS Compatibility: <Good / Moderate / Poor>

Key Strengths:
- <strength 1 from this resume>
- <strength 2>
- <strength 3>
- <strength 4>
- <strength 5>

Weaknesses or Missing Sections:
- <weakness 1>
- <weakness 2>
- <weakness 3>
- <weakness 4>
- <weakness 5>

Clear Improvement Suggestions:
- <actionable suggestion 1>
- <actionable suggestion 2>
- <actionable suggestion 3>
- <actionable suggestion 4>
- <actionable suggestion 5>

Resume Content:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict professional ATS resume evaluator. Every response must be specific to the provided resume.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,  # 🔥 Slight variation but still stable
        )

        return response.choices[0].message.content

    except Exception as e:
        # 🔥 Show real backend error (helps debugging in frontend)
        print("\n===== OPENAI ERROR =====")
        print(str(e))
        print("========================\n")

        return f"AI processing error: {str(e)}"
