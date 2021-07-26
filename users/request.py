import sqlite3
from database import DB_FILE
from models import User

def get_user_by_email(email):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            WHERE email = ?
        """, (email,))

        dataset = db_cursor.fetchone()

        return User(
            dataset['id'],
            dataset['first_name'],
            dataset['last_name'],
            dataset['email'],
            dataset['bio'],
            dataset['username'],
            dataset['password'],
            dataset['profile_image_url'],
            dataset['created_on'],
            dataset['active']
        ).__dict__