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
# MYSQL CONNECTION (AIVEN + RENDER COMPATIBLE)
# =========================================

def get_db_connection():
    # 1. First Priority: Check Render DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        url = urllib.parse.urlparse(db_url)
        return mysql.connector.connect(
            host=url.hostname,
            port=url.port or 23476,
            user=url.username,
            password=url.password,
            database=url.path.lstrip('/'),
            ssl_disabled=False
        )

    # 2. Second Priority: Fallback to Individual Environment Variables
    host = os.getenv("DB_HOST") or os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST")
    user = os.getenv("DB_USER") or os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER")
    password = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_PASSWORD")
    database = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DATABASE") or "careerverse"
    port_env = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or "23476"

    return mysql.connector.connect(
        host=host,
        port=int(port_env),
        user=user,
        password=password,
        database=database,
        ssl_disabled=False
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
# FRONTEND STATIC FILES (CSS/JS)
# =========================================

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(
        FRONTEND_FOLDER,
        filename
    )


# =========================================
# GET ALL QUESTIONS API
# =========================================

@app.route("/api/questions")
def get_questions():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

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
# CAREER RECOMMENDATION API
# =========================================

@app.route("/api/recommend", methods=["POST"])
def recommend_career():
    data = request.get_json()
    answers = data.get("answers", [])

    if not answers:
        return jsonify({"error": "No answers received"}), 400

    # Count category scores
    scores = {}
    for answer in answers:
        category = answer.get("category")
        if category:
            scores[category] = scores.get(category, 0) + 1

    if not scores:
        return jsonify({"error": "Invalid answers"}), 400

    # Find highest score
    best_category = max(scores, key=scores.get)

    # Fetch recommendations from DB
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

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