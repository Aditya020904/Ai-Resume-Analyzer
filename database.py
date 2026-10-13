import sqlite3
import json


DATABASE_NAME = "resume_analyzer.db"


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            match_score REAL,
            matched_skills TEXT,
            missing_skills TEXT
        )
    """)

    connection.commit()

    connection.close()


# =========================================================
# SAVE ANALYSIS
# =========================================================

def save_analysis(
    resume_name,
    match_score,
    matched_skills,
    missing_skills
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            resume_name,
            match_score,
            matched_skills,
            missing_skills
        )
        VALUES (?, ?, ?, ?)
    """, (
        resume_name,
        match_score,
        json.dumps(matched_skills),
        json.dumps(missing_skills)
    ))

    connection.commit()

    connection.close()


# =========================================================
# GET ALL ANALYSES
# =========================================================

def get_all_analyses():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            resume_name,
            match_score,
            matched_skills,
            missing_skills
        FROM analyses
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results