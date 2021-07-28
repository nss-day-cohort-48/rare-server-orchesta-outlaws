import sqlite3
import json
from models import Comment, Post
from datetime import datetime

def get_all_comments():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content,
            p.category_id category_id,
            p.title subject_title,
            p.publication_date publication_date,
            p.image_url image_url,
            p.content content,
            p.approved approved
        FROM Comments c
        JOIN Posts p
            ON p.id = c.post_id
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])
            
            post = Post(row['id'], row['author_id'], row['category_id'], row['subject_title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
           
            comment.title = post.__dict__
            
            comments.append(comment.__dict__)

    return comments

def create_comment(new_comment):
    '''Reader/Author can add a comment to an author's post. Resulting comment will display the article title and content'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id, author_id, content )
        VALUES
            ( ?, ?, ?);
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content'], )) 

        id = db_cursor.lastrowid
        new_comment['id'] = id

    return new_comment

def view_comments_by_post(postID):
    '''Reader can see a list of all the comments on a post'''
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.post_id,
            c.author_id,
            c.content
        FROM Comments c
        WHERE c.post_id = ?
        """, (postID, ))

        comments = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:

            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])
            comments.append(comment.__dict__)
        
        return comments

def delete_comment(id):
    '''Reader can delete a comment they have made'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))
    

def edit_comment(id, new_comment):
    '''Reader can edit a comment they have made'''
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Comments
            SET
                post_id = ?,
                author_id = ?,
                content = ?
        WHERE id = ?
        """, (new_comment['post_id'], new_comment['author_id'],
              new_comment['content'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True