from ai_recommendations import ask_llm


def recommend_roles(resume_text):

    prompt = f"""
You are a career recommendation system.

Analyze this resume:

{resume_text}

Recommend the 5 most suitable job roles.

For each role provide:

1. Job Role
2. Match Percentage
3. Short Reason

Use this format:

1. Data Analyst - 89%
Reason: ...

2. Python Developer - 82%
Reason: ...

3. Machine Learning Engineer - 71%
Reason: ...

Only recommend roles that are reasonably supported
by the candidate's resume.
Do not invent qualifications.
"""

    return ask_llm(prompt)