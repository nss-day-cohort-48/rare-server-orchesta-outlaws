import sqlite3
from database import DB_FILE
from models import Post, Category, User


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
            c.label category_label
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
            category = Category(row['id'], row['category_label'])
            post.category = category.__dict__
            posts.append(post.__dict__)

    return posts


def get_subbed_posts_for_user(id):
    """Returns a list of user_ids that the user for the provided id is subbed to."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT s.author_id,
                p.*,
                u.id user_id, u.first_name, u.last_name,
                c.label category_label
            FROM Subscriptions s
                JOIN Posts p ON p.user_id = s.author_id
                JOIN Categories c ON p.category_id = c.id
                LEFT JOIN Users u ON p.user_id = u.id
            WHERE s.follower_id = ?;
        """, (id,))

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['image_url'],
                        row['content'], row['approved'])
            category = Category(row['id'], row['category_label'])
            post.category = category.__dict__
            post.user = { 
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
            }
            posts.append(post.__dict__)

        return posts
