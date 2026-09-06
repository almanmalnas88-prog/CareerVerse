import os
import urllib.parse
import mysql.connector

def get_db_connection():
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
    
    return mysql.connector.connect(
        host=os.getenv("DB_HOST") or os.getenv("MYSQLHOST"),
        port=int(os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or 23476),
        user=os.getenv("DB_USER") or os.getenv("MYSQLUSER"),
        password=os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD"),
        database=os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE") or "careerverse"
    )
