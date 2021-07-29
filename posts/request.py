import sqlite3
from database import DB_FILE
from models import Post, Category, User


def get_all_posts():
    """Returns a list of all the posts from the Post table
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
            c.label category_label,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM posts p
        JOIN users u
            ON p.user_id = u.id
        JOIN categories c
            ON p.category_id = c.id
        """)
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                            row['title'], row['publication_date'], row['image_url'],
                            row['content'], row['approved'])

            user = User(row['user_id'], row['first_name'], row['last_name'], row['email'],
                            row['bio'], row['username'], row['password'],
                            row['profile_image_url'], row['created_on'], row['active'])
            post.user = user.__dict__

            category = Category(row['category_id'], row['category_label'])
            post.category = category.__dict__

            posts.append(post.__dict__)

    return posts


def get_single_post(id):
    """Get a single post by its id
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
            c.label category_label,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM posts p
        JOIN users u
            ON p.user_id = u.id
        JOIN categories c
            ON p.category_id = c.id
        WHERE p.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'],
                            data['title'], data['publication_date'], data['image_url'],
                            data['content'], data['approved'])

        user = User(data['user_id'], data['first_name'], data['last_name'], data['email'],
                            data['bio'], data['username'], data['password'],
                            data['profile_image_url'], data['created_on'], data['active'])
        post.user = user.__dict__

        category = Category(data['category_id'], data['category_label'])
        post.category = category.__dict__

    return post.__dict__


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
            category = Category(row['category_id'], row['category_label'])
                        row['title'], row['publication_date'], row['image_url'],
                        row['content'], row['approved'])
            post.category = category.__dict__
            posts.append(post.__dict__)

    return posts


def create_post(new_post):
    """adds a new post to the Posts table
    """
    with sqlite3.connect(DB_FILE) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'], new_post['title'],
                new_post['publication_date'], new_post['image_url'],
                new_post['content'], new_post['approved']))

        id = db_cursor.lastrowid
        new_post['id'] = id


    return new_post


def update_post(id, new_post):
    """update a post in the database
    """
    with sqlite3.connect(DB_FILE) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'], new_post['title'],
                new_post['publication_date'], new_post['image_url'],
                new_post['content'], new_post['approved'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_post(id):
    """delete a post from the database
    """
    with sqlite3.connect(DB_FILE) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))

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
