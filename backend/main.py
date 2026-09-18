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
# MYSQL CONNECTION
# AIVEN + RENDER COMPATIBLE
# =========================================

def get_db_connection():

    # -----------------------------------------
    # 1. DATABASE_URL
    # -----------------------------------------

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


    # -----------------------------------------
    # 2. INDIVIDUAL ENVIRONMENT VARIABLES
    # -----------------------------------------

    host = (
        os.getenv("DB_HOST")
        or os.getenv("MYSQLHOST")
        or os.getenv("MYSQL_HOST")
    )

    user = (
        os.getenv("DB_USER")
        or os.getenv("MYSQLUSER")
        or os.getenv("MYSQL_USER")
    )

    password = (
        os.getenv("DB_PASSWORD")
        or os.getenv("MYSQLPASSWORD")
        or os.getenv("MYSQL_PASSWORD")
    )

    database = (
        os.getenv("DB_NAME")
        or os.getenv("MYSQLDATABASE")
        or os.getenv("MYSQL_DATABASE")
        or "careerverse"
    )

    port_env = (
        os.getenv("DB_PORT")
        or os.getenv("MYSQLPORT")
        or "23476"
    )


    return mysql.connector.connect(

        host=host,

        port=int(port_env),

        user=user,

        password=password,

        database=database,

        ssl_disabled=False
    )


# =========================================
# SAVE STUDENT INFORMATION API
# =========================================

@app.route("/api/student", methods=["POST"])
def save_student():

    try:

        # -----------------------------------------
        # GET DATA FROM FRONTEND
        # -----------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({
                "error": "No student data received"
            }), 400


        # -----------------------------------------
        # GET INDIVIDUAL VALUES
        # -----------------------------------------

        name = data.get("name")

        age = data.get("age")

        education = data.get("education")

        city = data.get("city")

        family_occupation = data.get(
            "family_occupation"
        )


        # -----------------------------------------
        # NAME IS REQUIRED
        # -----------------------------------------

        if not name:

            return jsonify({
                "error": "Name is required"
            }), 400


        # -----------------------------------------
        # CONNECT TO MYSQL
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor()


        # -----------------------------------------
        # INSERT STUDENT INTO DATABASE
        # -----------------------------------------

        cursor.execute("""

            INSERT INTO students
            (
                name,
                age,
                education,
                city,
                family_occupation
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )

        """, (

            name,

            age,

            education,

            city,

            family_occupation

        ))


        # -----------------------------------------
        # SAVE CHANGES
        # -----------------------------------------

        connection.commit()


        # -----------------------------------------
        # CLOSE CONNECTION
        # -----------------------------------------

        cursor.close()

        connection.close()


        # -----------------------------------------
        # SUCCESS RESPONSE
        # -----------------------------------------

        return jsonify({

            "message":
                "Student saved successfully"

        })


    except Exception as error:

        print(
            "Student save error:",
            error
        )

        return jsonify({

            "error":
                "Could not save student"

        }), 500


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
# FRONTEND STATIC FILES
# CSS / JS / MANIFEST / SERVICE WORKER
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

    try:

        # -----------------------------------------
        # CONNECT TO MYSQL
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # -----------------------------------------
        # GET QUESTIONS
        # -----------------------------------------

        cursor.execute("""

            SELECT
                id,
                question_text

            FROM questions

            ORDER BY id

        """)


        questions = cursor.fetchall()


        # -----------------------------------------
        # GET OPTIONS FOR EACH QUESTION
        # -----------------------------------------

        for question in questions:

            cursor.execute("""

                SELECT
                    id,
                    option_text,
                    category

                FROM options

                WHERE question_id = %s

                ORDER BY id

            """, (
                question["id"],
            ))


            question["options"] = (
                cursor.fetchall()
            )


        # -----------------------------------------
        # CLOSE CONNECTION
        # -----------------------------------------

        cursor.close()

        connection.close()


        # -----------------------------------------
        # RETURN QUESTIONS
        # -----------------------------------------

        return jsonify(
            questions
        )


    except Exception as error:

        print(
            "Question loading error:",
            error
        )

        return jsonify({

            "error":
                "Could not load questions"

        }), 500


# =========================================
# CAREER RECOMMENDATION API
# =========================================

@app.route(
    "/api/recommend",
    methods=["POST"]
)
def recommend_career():

    try:

        # -----------------------------------------
        # GET ANSWERS FROM FRONTEND
        # -----------------------------------------

        data = request.get_json()

        answers = data.get(
            "answers",
            []
        )


        # -----------------------------------------
        # CHECK ANSWERS
        # -----------------------------------------

        if not answers:

            return jsonify({

                "error":
                    "No answers received"

            }), 400


        # -----------------------------------------
        # COUNT CATEGORY SCORES
        # -----------------------------------------

        scores = {}


        for answer in answers:

            category = answer.get(
                "category"
            )


            if category:

                scores[category] = (
                    scores.get(
                        category,
                        0
                    ) + 1
                )


        # -----------------------------------------
        # CHECK SCORES
        # -----------------------------------------

        if not scores:

            return jsonify({

                "error":
                    "Invalid answers"

            }), 400


        # -----------------------------------------
        # FIND HIGHEST SCORE
        # -----------------------------------------

        best_category = max(
            scores,
            key=scores.get
        )


        # -----------------------------------------
        # CONNECT TO MYSQL
        # -----------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # -----------------------------------------
        # GET CAREERS
        # -----------------------------------------

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

        """, (
            best_category,
        ))


        careers = cursor.fetchall()


        # -----------------------------------------
        # CLOSE CONNECTION
        # -----------------------------------------

        cursor.close()

        connection.close()


        # -----------------------------------------
        # RETURN RESULT
        # -----------------------------------------

        return jsonify({

            "category":
                best_category,

            "scores":
                scores,

            "careers":
                careers

        })


    except Exception as error:

        print(
            "Recommendation error:",
            error
        )

        return jsonify({

            "error":
                "Could not calculate recommendation"

        }), 500


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )