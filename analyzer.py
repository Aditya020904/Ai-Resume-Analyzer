from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def calculate_similarity(resume_text, job_description):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    return round(similarity * 100, 2)


def analyze_resume(resume_text, job_description):
    score = calculate_similarity(
        resume_text,
        job_description
    )

    return {
        "overall_score": score
    }