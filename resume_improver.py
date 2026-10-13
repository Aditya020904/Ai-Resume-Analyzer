from ai_recommendations import ask_llm


def improve_resume(resume_text):

    prompt = f"""
You are a professional resume writer.

Improve the following resume content.

RESUME:
{resume_text}

Rewrite weak resume statements into strong,
professional, achievement-oriented statements.

Rules:

1. Do not invent experience.
2. Do not invent companies.
3. Do not invent degrees.
4. Do not invent technologies.
5. Keep the original meaning.
6. Make bullet points professional.
7. Use strong action verbs.
8. Add measurable results only when they already exist
   in the original resume.

Give the result in this format:

Current:
[original weak statement]

Suggested:
[improved statement]

Repeat this for the most important weak statements.
"""

    return ask_llm(prompt)