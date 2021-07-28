import sqlite3
from models import Tag, Post, PostTag

def get_all_tags():
    '''See all the tags stored in the db
    '''
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        """)
        
        tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['label'])
        
            tags.append(tag.__dict__)
    
    return tags

def create_tag(new_tag):
    '''Author can add a tag to the existing list of tags to better classify posts'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
            ( ?);
        """, (new_tag['label'], )) 

        id = db_cursor.lastrowid
        new_tag['id'] = id

    return new_tag

def add_tag_to_post(tag_post):
    '''Author is able to associate one or more Tags with one of their posts'''

def remove_tag(tag_id):
    '''Author is able to unassociate one or more Tags from their posts'''

def search_by_tag(search):
    '''Reader can find Posts by Tag name to more easily find relevant posts'''
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(f"""
        SELECT
            p.id,
            p.tag_id,
            p.post_id,
            t.label,
            a.user_id,
            a.category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content,
            a.approved
        FROM PostTags p
        JOIN Tags t
            ON t.id = p.tag_id
        JOIN Posts a
            ON a.id = p.post_id
        WHERE label LIKE "%{search}%"
        """)

        postTags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            postTag = PostTag(row['id'], row['tag_id'], row['post_id'])
            tag = Tag(row['id'], row['label'])
            post = Post(row['id'], row['author_id'], row['category_id'], row['subject_title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
            
            postTag.tag = tag.__dict__
            postTag.post = post.__dict__

            postTags.append(postTag.__dict__)

    return postTags