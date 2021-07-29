import sqlite3
from models import PostTag, Tag, Post

def search_post_by_tag(search):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(f"""
        SELECT
            a.id,
            a.tag_id,
            a.post_id,
            t.label label,
            p.user_id user_id,
            p.category_id category_id,
            p.title title,
            p.publication_date publication_date,
            p.image_url image_url,
            p.content content,
            p.approved approved
        FROM PostTags a
        JOIN Tags t
            ON t.id = a.tag_id
        JOIN Posts p
            ON p.id = a.post_id
        WHERE t.label LIKE "%{search}%"
        """)

        posttags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            posttag = PostTag(row['id'], row['tag_id'], row['post_id'])

            tag = Tag(row['id'], row['label'])
            
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['image_url'],
                        row['content'], row['approved'])

            posttag.label = tag.__dict__
            posttag.post = post.__dict__

            posttags.append(posttag.__dict__)

    return posttags

def get_all_posttags():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.tag_id,
            a.post_id,
            t.label label,
            p.user_id user_id,
            p.category_id category_id,
            p.title title,
            p.publication_date publication_date,
            p.image_url image_url,
            p.content content,
            p.approved approved
        FROM PostTags a
        JOIN Tags t
            ON t.id = a.tag_id
        JOIN Posts p
            ON p.id = a.post_id
        """)

        posttags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            posttag = PostTag(row['id'], row['tag_id'], row['post_id'])
            tag = Tag(row['id'], row['label'])
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['image_url'],
                        row['content'], row['approved'])

            posttag.label = tag.__dict__
            posttag.post = post.__dict__
            
            posttags.append(posttag.__dict__)

    return posttags

def add_tag_to_post(tag_post):
    '''Author is able to associate one or more Tags with one of their posts'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO PostTags
            ( post_id, tag_id )
        VALUES
            ( ?, ?);
        """, (tag_post['post_id'], tag_post['tag_id'], )) 

        id = db_cursor.lastrowid
        tag_post['id'] = id

    return tag_post

def remove_tag(tag_id):
    '''Author is able to unassociate one or more Tags from their posts'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM PostTags
        WHERE id = ?
        """, (tag_id, ))
