import sqlite3
from database import DB_FILE
from models import Post, Category

def get_posts_by_user(id):
    """Returns a list of all the posts by the user's id
    """
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.label comment_label
        FROM posts p
        JOIN categories c
            ON p.category_id = c.id
        WHERE p.user_id = ?
        """, (id, ))
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                            row['title'], row['publication_date'], row['image_url'],
                            row['content'], row['approved'])
            category = Category(row['id'], row['comment_label'])
            post.category = category.__dict__
            posts.append(post.__dict__)

    return posts

def get_user_subbed_posts(id):
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