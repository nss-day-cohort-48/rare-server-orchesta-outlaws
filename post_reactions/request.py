import sqlite3
from database import DB_FILE
from models import Post_Reaction

def get_all_post_reactions():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            pr.id,
            pr.user_id,
            pr.reaction_id,
            pr.post_id
        FROM PostReactions pr
        """)
        post_reactions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post_reaction = Post_Reaction(row['id'], row['user_id'], row['reaction_id'],
                            row['post_id'])
            post_reactions.append(post_reaction.__dict__)

    return post_reactions
