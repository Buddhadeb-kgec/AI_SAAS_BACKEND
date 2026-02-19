from dotenv import load_dotenv
import os
from pathlib import Path
from openai import OpenAI

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_text(text: str) -> str:
    """
    Analyze resume/document text using OpenAI ATS-style evaluation.
    """

    if not text or not text.strip():
        return "No readable text found in the uploaded file."

    try:
        print("\n===== TEXT SENT TO AI (first 500 chars) =====\n")
        print(text[:500])
        print("\n=============================================\n")

        prompt = f"""
You are a strict ATS resume evaluator and professional career coach.

Carefully analyze this specific resume/document and return:

Resume Score: <0–100>

ATS Compatibility: <Good / Moderate / Poor>

Key Strengths:
- ...
- ...
- ...
- ...
- ...

Weaknesses:
- ...
- ...
- ...
- ...
- ...

Improvement Suggestions:
- ...
- ...
- ...
- ...
- ...

Resume Content:
{text[:4000]}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict professional ATS resume evaluator. Every answer must be specific to the provided resume.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("\n===== OPENAI ERROR =====")
        print(str(e))
        print("========================\n")

        return f"AI processing error: {str(e)}"
