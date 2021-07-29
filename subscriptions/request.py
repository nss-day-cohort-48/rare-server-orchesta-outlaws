import sqlite3
from database import DB_FILE

def get_sub_posts(id):
    """Returns a list of user_ids that the user for the provided id is subbed to."""
    with sqlite3.connect(DB_FILE) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT s.author_id, p.*
            FROM Subscriptions s
            WHERE s.follower_id = ?
            JOIN Posts p
            ON p.user_id = s.author_id
        """, (id,))
    
        dataset = db_cursor.fetchall()
        # TODO: build and return the posts