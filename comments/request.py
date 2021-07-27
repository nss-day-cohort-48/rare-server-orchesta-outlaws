import sqlite3
import json
from models import Comment
from datetime import datetime

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