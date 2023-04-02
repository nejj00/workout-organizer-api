import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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
#connection = psycopg2.connect(url)

url_alchemy = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(app)
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

@app.get("/api/categories")
def get_all_categories():
    categories = Category.query.all()
    category_list = []
    for category in categories:
        category_list.append({'id': category.id, 'name': category.name})

    return jsonify({'categories': category_list})