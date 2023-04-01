import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_CATEGORIES_TABLE = (
    "CREATE TABLE IF NOT EXISTS categories (id SERIAL PRIMARY KEY, name TEXT);"
)

INSERT_CATEGORY_RETURN_ID = (
    "INSERT INTO categories (name) VALUES (%s) RETURNING id;"
)

GET_ALL_CATEGORIES = (
    "SELECT * FROM categories;"
)

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/category")
def create_category():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CATEGORIES_TABLE)
            cursor.execute(INSERT_CATEGORY_RETURN_ID, (name,))
            category_id = cursor.fetchone()[0]
    return {"id": category_id, "message": f"Category {name} created."}, 201


@app.get("/api/categories")
def get_all_categories():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ALL_CATEGORIES)
            categories = cursor.fetchall()
    
    return categories