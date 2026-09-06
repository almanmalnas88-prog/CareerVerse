from flask import Flask, send_from_directory, jsonify, request
import mysql.connector
import os
import urllib.parse
from dotenv import load_dotenv


# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()


# =========================================
# CREATE FLASK APP
# =========================================

app = Flask(__name__)


# =========================================
# FRONTEND LOCATION
# =========================================

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "frontend"
    )
)


# =========================================
# MYSQL CONNECTION (UPDATED FOR RENDER & AIVEN)
# =========================================

def get_db_connection():
    # 1. Check if Render DATABASE_URL exists
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        url = urllib.parse.urlparse(db_url)
        return mysql.connector.connect(
            host=url.hostname,
            port=url.port or 23476,
            user=url.username,
            password=url.password,
            database=url.path.lstrip('/')
        )

    # 2. Fallback to individual Environment Variables
    return mysql.connector.connect(
        host=os.getenv("DB_HOST") or os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST"),
        port=int(os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or 23476),
        user=os.getenv("DB_USER") or os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER"),
        password=os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DATABASE") or "careerverse"
    )


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_FOLDER,
        "index.html"
    )


# =========================================
# CSS / JS / OTHER FRONTEND FILES
# =========================================

@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_FOLDER,
        filename
    )


# =========================================
# GET ALL QUESTIONS
# =========================================

@app.route("/api/questions")
def get_questions():

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT
            id,
            question_text
        FROM questions
        ORDER BY id
    """)

    questions = cursor.fetchall()


    for question in questions:

        cursor.execute("""
            SELECT
                id,
                option_text,
                category
            FROM options
            WHERE question_id = %s
            ORDER BY id
        """, (question["id"],))

        question["options"] = cursor.fetchall()


    cursor.close()

    connection.close()


    return jsonify(questions)


# =========================================
# CAREER RECOMMENDATION
# =========================================

@app.route(
    "/api/recommend",
    methods=["POST"]
)
def recommend_career():

    data = request.get_json()

    answers = data.get(
        "answers",
        []
    )


    if not answers:

        return jsonify({
            "error": "No answers received"
        }), 400


    # =====================================
    # COUNT CATEGORY SCORES
    # =====================================

    scores = {}


    for answer in answers:

        category = answer.get(
            "category"
        )


        if category:

            scores[category] = (
                scores.get(category, 0) + 1
            )


    if not scores:

        return jsonify({
            "error": "Invalid answers"
        }), 400


    # =====================================
    # FIND HIGHEST SCORE
    # =====================================

    best_category = max(
        scores,
        key=scores.get
    )


    # =====================================
    # FIND CAREERS FROM DATABASE
    # =====================================

    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute("""
        SELECT
            id,
            name,
            category,
            description,
            education_required,
            skills_required
        FROM careers
        WHERE category = %s
        LIMIT 5
    """, (best_category,))


    careers = cursor.fetchall()


    cursor.close()

    connection.close()


    # =====================================
    # SEND RESULT TO JAVASCRIPT
    # =====================================

    return jsonify({

        "category": best_category,

        "scores": scores,

        "careers": careers

    })


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
