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
            p.subject comment_subject
        FROM Comments c
        JOIN Posts p
            ON p.id = c.post_id
        """)

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'], row['content'])

            subject = Post(row['post_id'], row['user_id'], row['category_id'],
                            row['title'], row['publication_date'], row['image_url'],
                            row['content'], row['approved'])
            
            comment.subject = subject.__dict__

            comments.append(comment.__dict__)

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
      db_cursor = conn.cursor()

      db_cursor.execute("""
      SELECT
        c.id
        c.post_id
        c.author_id
        c.content
      FROM Comments c
      WHERE c.post_id = ?
      """, ( postID, ))

      comments = []
      dataset = db_cursor.fetchall()

      for row in dataset:
            comment = Comment(row['id'], row['post_id'], row['author_id'],row['content'])
            comments.append(comment.__dict__)

    return comments

def delete_comment(comment_id):
    '''Reader can delete a comment they have made'''

def edit_comment(comment_id):
    '''Reader can edit a comment they have made'''