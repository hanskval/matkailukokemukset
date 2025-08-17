import db
import sqlite3
def add_item(title, description, rating, user_id, category):
    sql = """INSERT INTO experiences (title, description, user_id, rating) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, user_id, rating])
    item_id = db.last_insert_id()
    if category:
        sql = "INSERT INTO categories (item_id, title) VALUES (?, ?)"
        db.execute(sql, [item_id, category])
        
def get_categories(item_id):
    sql = "SELECT title FROM categories WHERE item_id = ? LIMIT 1"
    results = db.query(sql, [item_id])
    return results[0][0] if results else None


def get_items():
    sql = "SELECT * FROM experiences"
    return db.query(sql)

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if result:
        return result[0][0]
    return None

def insert_user(username, password_hash):
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_password(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    results = db.query(sql, [username])
    if results:
        return results[0][0]
    return None

def comment_experience(user_id, item_id, comment):
    sql = "INSERT INTO comments (user_id, item_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, item_id, comment])
    
def get_comments(item_id):
    sql = """SELECT comments.id, comments.comment, comments.created_at, comments.user_id, users.username
             FROM comments, users
             WHERE comments.user_id = users.id AND comments.item_id = ?"""
    return db.query(sql, [item_id,])

def get_items_by_user(username):
    sql = """SELECT experiences.id,
                    experiences.title,
                    experiences.description,
                    experiences.rating,
                    users.username
             FROM experiences, users
             WHERE experiences.user_id = users.id AND users.username = ?"""
    return db.query(sql, [username])

def has_liked(user_id, experience_id): # Tarkistaa onko tykätty kokemuksesta
    sql = "SELECT 1 FROM likes WHERE user_id = ? AND experience_id = ?"
    result = db.query(sql, [user_id, experience_id])
    return len(result) > 0

def add_like(user_id, experience_id): # Lisää tykkäyksen kokemukseen
    sql = "INSERT INTO likes (user_id, experience_id) VALUES (?, ?)"
    db.execute(sql, [user_id, experience_id])

def remove_like(user_id, experience_id): # Poistaa tykkäyksen kokemuksesta
    sql = "DELETE FROM likes WHERE user_id = ? AND experience_id = ?"
    db.execute(sql, [user_id, experience_id])

def get_likes_count(experience_id):
    sql = "SELECT COUNT(*) FROM likes WHERE experience_id = ?"
    result = db.query(sql, [experience_id])
    return result[0][0] if result else 0

def get_item(item_id):
    sql = """SELECT experiences.id,
                    experiences.title,
                     experiences.description,
                     experiences.rating,
                     users.id AS user_id,
                     users.username
                FROM experiences, users
                WHERE experiences.user_id = users.id AND experiences.id = ?"""

    results = db.query(sql, [item_id])
    return results[0] if results else None

def update_item(item_id, title, description, rating, category):
    sql = """UPDATE experiences
             SET title = ?, description = ?, rating = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, rating, item_id])
    if category:
        sql = """UPDATE categories
                 SET title = ?
                 WHERE item_id = ?"""
    db.execute(sql, [category, item_id])

def remove_item(item_id):
    with db.get_connection() as con:
        con.execute("DELETE FROM categories WHERE item_id = ?", [item_id])
        con.execute("DELETE FROM comments WHERE item_id = ?", [item_id])
        con.execute("DELETE FROM likes WHERE experience_id = ?", [item_id])# poistaa ensin tykkäykset jonka jälkeen voi poistaa kokemuksen
        con.execute("DELETE FROM experiences WHERE id = ?", [item_id])


def find_kokemuksia(query, ratings):
    sql = "SELECT id, title, description, rating FROM experiences WHERE 1=1"
    params = []
    
    if ratings:
        placeholders = ",".join(["?"] * len(ratings))
        sql += f" AND rating IN ({placeholders})"
        params.extend(ratings)

    if query:
        sql += " AND (LOWER(title) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))"
        params.extend([f"%{query}%", f"%{query}%"])


    return db.query(sql, params)
