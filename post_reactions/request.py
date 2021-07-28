import sqlite3
from models.post_reactions import PostReaction
from models.reactions import Reaction
















































def get_post_reactions_by_post_id(post_id):
    with sqlite3.connect("./rare.db") as conn:
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
