import db
def add_item(title, description, rating, user_id):
    sql = """INSERT INTO experiences (title, description, user_id, rating) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, user_id, rating])

def get_items():
    sql = "SELECT * FROM experiences"
    return db.query(sql)

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

def remove_like(user_id, experience_id):
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

def update_item(item_id, title, description, rating):
    sql = """UPDATE experiences
             SET title = ?, description = ?, rating = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, rating, item_id])

def remove_item(item_id):
    sql = "DELETE FROM experiences WHERE id = ?"
    db.execute(sql, [item_id])

def find_kokemuksia(query, ratings):
    sql = "SELECT * FROM experiences WHERE 1=1"
    params = []
    
    if ratings:
        placeholders = ",".join(["?"] * len(ratings))
        sql += f" AND rating IN ({placeholders})"
        params.extend(ratings)

    if query:
        sql += " AND (LOWER(title) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))"
        params.extend([f"%{query}%", f"%{query}%"])


    return db.query(sql, params)
