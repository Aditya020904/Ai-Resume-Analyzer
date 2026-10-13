from ai_recommendations import ask_llm


def generate_interview_questions(
    resume_text,
    job_description
):

    prompt = f"""
You are an experienced technical interviewer.

Generate interview questions based on the resume
and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Create:

TECHNICAL QUESTIONS

1. ...
2. ...
3. ...
4. ...
5. ...

HR QUESTIONS

1. ...
2. ...
3. ...
4. ...
5. ...

PROJECT QUESTIONS

1. ...
2. ...
3. ...

Questions should be relevant to the candidate's
actual resume and the job description.
"""

    return ask_llm(prompt)