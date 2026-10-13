import re


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS = [
    "python",
    "java",
    "c++",
    "c#",
    "c",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "react.js",
    "node.js",
    "express",
    "angular",
    "vue",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "ml",
    "nlp",
    "natural language processing",
    "computer vision",
    "tensorflow",
    "pytorch",
    "keras",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "langchain",
    "generative ai",
    "generative artificial intelligence",
    "llm",
    "large language model",
    "data science",
    "data analysis",
    "power bi",
    "tableau",
    "excel",
    "streamlit"
]


# =========================================================
# FIND SKILLS
# =========================================================

def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        # Escape special characters such as + and .
        escaped_skill = re.escape(skill)

        # Match complete words/phrases
        pattern = r"(?<!\w)" + escaped_skill + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills