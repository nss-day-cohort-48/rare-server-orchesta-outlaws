import sqlite3
from models import Tag

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

