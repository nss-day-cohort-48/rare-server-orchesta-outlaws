import sqlite3
from models import Reaction, PostReaction
from database import DB_FILE

def get_post_reactions_by_post_id(post_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            a.reaction_id,
            a.post_id,
            b.label reaction_label,
            b.image_url imageURL
        FROM PostReactions a
        JOIN Reactions b
            ON b.id = a.reaction_id
        WHERE a.post_id = ?;
        """, ( post_id, ))
        post_reactions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post_react = PostReaction(row["id"], row["user_id"], row["reaction_id"], row["post_id"])
            react_proper = Reaction(row["id"], row["reaction_label"], row["imageURL"])
            post_react.reaction = react_proper.__dict__
            post_reactions.append(post_react.__dict__)
        return post_reactions

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
            post_reaction = PostReaction(row['id'], row['user_id'], row['reaction_id'],
                            row['post_id'])
            post_reactions.append(post_reaction.__dict__)
    return post_reactions

def create_post_reaction(new_post_reaction):
    with sqlite3.connect(DB_FILE) as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO PostReactions
            (user_id, reaction_id, post_id)
        VALUES
            (?, ?, ?)
        """, (new_post_reaction["user_id"], new_post_reaction["reaction_id"], new_post_reaction["post_id"], ))
        id = db_cursor.lastrowid
        new_post_reaction["id"] = id
    return new_post_reaction