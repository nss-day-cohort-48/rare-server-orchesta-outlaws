from models.category import Category
import sqlite3
import json

def get_all_categories():
    """fetch call to GET all categories; available now to all users; in future, only for admin side
    """
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.label
        FROM Categories a
        """)
        categories = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            category = Category(row["id"], row["label"])
            categories.append(category.__dict__)
    return categories

def create_category(new_cat):
    """creates a new category, id associated with foreign key in Posts table
    """
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Categories
            (label)
        VALUES
            (?)
        """, (new_cat["label"], ))
        id = db_cursor.lastrowid
        new_cat["id"] = id
    return json.dumps(new_cat)
