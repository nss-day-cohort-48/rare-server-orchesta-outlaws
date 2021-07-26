import sqlite3
import json

def create_comment(new_comment):
    '''Reader/Author can add a comment to an author's post'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db.cursor.execute("""
        INSERT INTO Comments
            ( post_id, author_id, content )
        VALUES
            ( ?, ?, ?);
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content'], )) 

        id = db_cursor.lastrowid
        new_comment['id'] = id

    return json.dumps(new_comment)

def view_post_comments(postID):
    '''Reader can see a list of all the comments on a post'''

def delete_comment(comment_id):
    '''Reader can delete a comment they have made'''

def edit_comment(comment_id):
    '''Reader can edit a comment they have made'''