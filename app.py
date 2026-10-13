import streamlit as st

from analyzer import (
    extract_text_from_pdf,
    calculate_similarity
)

from skills import find_skills

from database import (
    create_database,
    save_analysis
)

from ai_recommendations import generate_recommendations
from resume_improver import improve_resume
from role_recommender import recommend_roles
from interview import generate_interview_questions


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

create_database()


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "job_description" not in st.session_state:
    st.session_state.job_description = ""

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "job_skills" not in st.session_state:
    st.session_state.job_skills = []

if "matched_skills" not in st.session_state:
    st.session_state.matched_skills = []

if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []

if "similarity_score" not in st.session_state:
    st.session_state.similarity_score = 0

if "skill_match_score" not in st.session_state:
    st.session_state.skill_match_score = 0

if "overall_score" not in st.session_state:
    st.session_state.overall_score = 0

if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📄 AI Resume Analyzer")

st.write(
    "Analyze your resume against a job description "
    "using NLP, semantic similarity and AI."
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

resume_file = st.file_uploader(
    "Upload your Resume PDF",
    type=["pdf"]
)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the complete job description here..."
)


# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

if st.button("🔍 Analyze Resume"):

    if resume_file is None:

        st.warning("Please upload a resume PDF.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        with st.spinner("Analyzing resume..."):

            # Extract resume text
            resume_text = extract_text_from_pdf(
                resume_file
            )

            # Find skills in resume
            resume_skills = find_skills(
                resume_text
            )

            # Find skills in job description
            job_skills = find_skills(
                job_description
            )

            # AI semantic similarity
            similarity_score = calculate_similarity(
                resume_text,
                job_description
            )

            # Matched skills
            matched_skills = []

            for skill in job_skills:

                if skill in resume_skills:
                    matched_skills.append(skill)

            # Missing skills
            missing_skills = []

            for skill in job_skills:

                if skill not in resume_skills:
                    missing_skills.append(skill)

            # Skill match percentage
            if len(job_skills) > 0:

                skill_match_score = (
                    len(matched_skills)
                    / len(job_skills)
                ) * 100

            else:

                skill_match_score = 0

            # Overall score
            overall_score = (
                skill_match_score * 0.70
                + similarity_score * 0.30
            )

            overall_score = round(
                overall_score,
                2
            )

            # Save everything in session state
            st.session_state.resume_text = resume_text

            st.session_state.job_description = job_description

            st.session_state.resume_skills = resume_skills

            st.session_state.job_skills = job_skills

            st.session_state.matched_skills = matched_skills

            st.session_state.missing_skills = missing_skills

            st.session_state.similarity_score = similarity_score

            st.session_state.skill_match_score = round(
                skill_match_score,
                2
            )

            st.session_state.overall_score = overall_score

            st.session_state.resume_name = resume_file.name

            st.session_state.analysis_done = True

            # Save to database
            save_analysis(
                resume_file.name,
                overall_score,
                matched_skills,
                missing_skills
            )

        st.success("✅ Resume analysis completed!")


# ==================================================
# RESULTS
# ==================================================

if st.session_state.analysis_done:

    # --------------------------------------------------
    # PROFESSIONAL DASHBOARD
    # --------------------------------------------------

    st.divider()

    st.header("📊 Professional Resume Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Overall ATS",
            f"{st.session_state.overall_score}%"
        )

    with col2:

        st.metric(
            "Skill Match",
            f"{st.session_state.skill_match_score}%"
        )

    with col3:

        st.metric(
            "AI Similarity",
            f"{st.session_state.similarity_score}%"
        )

    with col4:

        st.metric(
            "Matched Skills",
            len(st.session_state.matched_skills)
        )


    # --------------------------------------------------
    # MATCHED AND MISSING SKILLS
    # --------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("✅ Matched Skills")

        if st.session_state.matched_skills:

            for skill in st.session_state.matched_skills:

                st.write(
                    f"✅ {skill.title()}"
                )

        else:

            st.write(
                "No matching skills found."
            )


    with col2:

        st.subheader("❌ Missing Skills")

        if st.session_state.missing_skills:

            for skill in st.session_state.missing_skills:

                st.write(
                    f"❌ {skill.title()}"
                )

        else:

            st.write(
                "No major missing skills found."
            )


    # --------------------------------------------------
    # RESUME SKILLS
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Skills Found in Resume")

    if st.session_state.resume_skills:

        st.write(
            ", ".join(
                skill.title()
                for skill in st.session_state.resume_skills
            )
        )

    else:

        st.write(
            "No skills detected."
        )


    # --------------------------------------------------
    # JOB REQUIRED SKILLS
    # --------------------------------------------------

    st.subheader("💼 Skills Required by Job")

    if st.session_state.job_skills:

        st.write(
            ", ".join(
                skill.title()
                for skill in st.session_state.job_skills
            )
        )

    else:

        st.write(
            "No specific skills detected from job description."
        )


    # --------------------------------------------------
    # AI RECOMMENDATIONS
    # --------------------------------------------------

    st.divider()

    st.header("🤖 AI Recommendations")

    if st.button("Generate AI Recommendations"):

        with st.spinner(
            "AI is analyzing your resume..."
        ):

            recommendations = generate_recommendations(
                st.session_state.resume_text,
                st.session_state.job_description,
                st.session_state.matched_skills,
                st.session_state.missing_skills
            )

        st.markdown(recommendations)


    # --------------------------------------------------
    # RESUME IMPROVEMENT
    # --------------------------------------------------

    st.divider()

    st.header("✍️ Resume Improvement")

    st.write(
        "AI will identify weak statements and suggest "
        "stronger professional versions."
    )

    if st.button("Improve My Resume"):

        with st.spinner(
            "Improving your resume..."
        ):

            improved_resume = improve_resume(
                st.session_state.resume_text
            )

        st.markdown(improved_resume)


    # --------------------------------------------------
    # JOB ROLE RECOMMENDATION
    # --------------------------------------------------

    st.divider()

    st.header("💼 Job Role Recommendation")

    st.write(
        "Find job roles that best match your resume."
    )

    if st.button("Recommend Suitable Jobs"):

        with st.spinner(
            "Finding suitable job roles..."
        ):

            roles = recommend_roles(
                st.session_state.resume_text
            )

        st.markdown(roles)


    # --------------------------------------------------
    # INTERVIEW QUESTIONS
    # --------------------------------------------------

    st.divider()

    st.header("🎤 Interview Question Generator")

    st.write(
        "Generate technical, HR and project-based "
        "interview questions."
    )

    if st.button("Generate Interview Questions"):

        with st.spinner(
            "Generating interview questions..."
        ):

            questions = generate_interview_questions(
                st.session_state.resume_text,
                st.session_state.job_description
            )

        st.markdown(questions)