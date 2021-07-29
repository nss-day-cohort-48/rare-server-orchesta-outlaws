import sqlite3
from database import DB_FILE

def get_sub_ids(id):
    """Returns a list of user_ids that the user for the provided id is subbed to."""
    with sqlite3.connect(DB_FILE) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT s.author_id
            FROM Subscriptions s
            WHERE s.follower_id = ?
        """, (id,))
    
        author_ids = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            author_ids.append(row['author_id'])
        return author_ids