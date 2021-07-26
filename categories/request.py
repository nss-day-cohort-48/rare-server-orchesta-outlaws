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
            category = Category(row['id'], row['label'])
            categories.append(category.__dict__)
    return json.dumps(categories)