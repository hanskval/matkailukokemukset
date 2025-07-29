import db
def add_item(title, description, rating, user_id):
    sql = """INSERT INTO experiences (title, description, user_id, rating) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, user_id, rating])

def get_items():
    sql = "SELECT * FROM experiences"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT experiences.id,
                    experiences.title,
                     experiences.description,
                     experiences.rating,
                     users.id AS user_id,
                     users.username
                FROM experiences, users
                WHERE experiences.user_id = users.id AND experiences.id = ?"""

    return db.query(sql, [item_id])[0]

def update_item(item_id, title, description, rating):
    sql = """UPDATE experiences
             SET title = ?, description = ?, rating = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, rating, item_id])
    
def remove_item(item_id):
    sql = "DELETE FROM experiences WHERE id = ?"
    db.execute(sql, [item_id])