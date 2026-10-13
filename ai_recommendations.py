import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def ask_llm(prompt):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")

    except Exception as e:

        return f"AI Error: {str(e)}"


def generate_recommendations(
    resume_text,
    job_description,
    matched_skills,
    missing_skills
):

    prompt = f"""
You are an expert resume reviewer.

Analyze the following resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

MATCHED SKILLS:
{matched_skills}

MISSING SKILLS:
{missing_skills}

Give a professional analysis with exactly these sections:

Resume Strengths
- Give 3 to 5 points.

Resume Weaknesses
- Give 3 to 5 points.

Missing Skills
- Explain the most important missing skills.

Improvement Suggestions
- Give 5 practical suggestions.

Keep the answer concise and useful for a job applicant.
"""

    return ask_llm(prompt)