import db
def add_item(title, description, rating, user_id):
    sql = """INSERT INTO experiences (title, description, user_id, rating) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, user_id, rating])
    
def get_items():
    sql = "SELECT * FROM experiences"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT experiences.title,
                     experiences.description,
                     experiences.rating,
                     users.username
                FROM experiences, users
                WHERE experiences.user_id = users.id AND experiences.id = ?"""

    return db.query(sql, [item_id])[0]