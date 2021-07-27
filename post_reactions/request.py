import sqlite3
from models.post_reactions import PostReaction

def get_post_reactions_by_post_id(post_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.reaction_id,
            a.post_id
        FROM PostReactions a
        WHERE a.post_id = ?
        """, ( post_id, ))
        post_reactions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post_react = PostReaction(row["id"], row["user_id"], row["reaction_id"], row["post_id"])
            post_reactions.append(post_react.__dict__)
    return post_reactions
