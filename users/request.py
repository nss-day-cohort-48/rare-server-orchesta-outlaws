import sqlite3
from datetime import datetime
from database import DB_FILE
from models import User


def login_user(email, password):
    """If the password is correct for the given email, returns the id"""
    user = get_user_by_email(email)
    if password == user['password']:
        return user['id']
    else:
        return None


def get_single_user(id):
    """get a single user by the user_id
        """
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            WHERE id = ?
        """, (id,))

        dataset = db_cursor.fetchone()

        return User(
            dataset['id'],
            dataset['first_name'],
            dataset['last_name'],
            dataset['email'],
            dataset['bio'],
            dataset['username'],
            dataset['password'],
            dataset['profile_image_url'],
            dataset['created_on'],
            dataset['active']
        ).__dict__


def get_user_by_email(email):
    """Get a single user by the email.
        """
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            WHERE email = ?
        """, (email,))

        dataset = db_cursor.fetchone()

        if dataset is None:
            return None
        else:
            return User(
                dataset['id'],
                dataset['first_name'],
                dataset['last_name'],
                dataset['email'],
                dataset['bio'],
                dataset['username'],
                dataset['password'],
                dataset['profile_image_url'],
                dataset['created_on'],
                dataset['active']
            ).__dict__


def create_new_user(user):
    """Create a new user given a dict containing all required keys"""
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            INSERT INTO Users
                (
                    first_name, 
                    last_name, 
                    email, 
                    bio, 
                    username, 
                    password, 
                    profile_image_url, 
                    created_on, 
                    active
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user['first_name'],
            user['last_name'],
            user['email'],
            user['bio'],
            user['username'],
            user['password'],
            user['profile_image_url'],
            user['created_on'],
            user['active']
        ))
        # Now that the INSERT is done, grab the autoincremented id
        user['id'] = db_cursor.lastrowid
        return user


def register_new_user(user):
    """Creates a new user in the database without a profile image URL or bio.
        """
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            INSERT INTO Users
                (
                    first_name, 
                    last_name, 
                    email, 
                    username, 
                    password, 
                    created_on, 
                    active
                )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user['first_name'],
            user['last_name'],
            user['email'],
            user['username'],
            user['password'],
            datetime.now().strftime("%Y-%m-%d"),
            1  # sets the "active" bit to 1 (True)
        ))
        # Now that the INSERT is done, grab the autoincremented id
        user['id'] = db_cursor.lastrowid
        return user
