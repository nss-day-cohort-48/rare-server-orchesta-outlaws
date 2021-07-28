import sqlite3

def create_reaction(new_reaction):
    """Creates a new reaction (for Admin use eventually)

    Args:
        new_reaction ([dict]): contains id and label (description)
    """
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Reactions
            (label, image_url)
        VALUES
            (?, ?)
        """, (new_reaction["label"], new_reaction["image_url"], ))
        id = db_cursor.lastrowid
        new_reaction["id"] = id
    return new_reaction