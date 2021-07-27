from models.category import Category
import sqlite3

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
    return new_cat

def update_category(id, new_cat):
    """PUT fetch call for Categories table

    Args:
        id ([int]): primary key
        new_cat ([dict]): dict containing key-value pairs for entire category entry
    """
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Categories
            SET
                label = ?
        WHERE id = ?
        """, (new_cat["label"], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True