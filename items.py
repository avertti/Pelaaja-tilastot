import db

def add_item(name, team, player_number, PPG, RPG, APG, user_id, classes):
    sql = """INSERT INTO items (name, team, player_number, PPG, RPG, APG, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [name, team, player_number, PPG, RPG, APG, user_id])

    item_id=db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def add_rating(item_id, user_id, rating):
    sql = """INSERT INTO ratings (item_id, user_id, rating) VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, user_id, rating])

def get_ratings(item_id):
    sql = """SELECT ratings.rating, users.id AS user_id,            users.username
           FROM ratings, users
           WHERE ratings.item_id = ? AND ratings.user_id = users.id
           ORDER BY ratings.id DESC"""
    return db.query(sql, [item_id])

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_items():
    sql = "SELECT id, name FROM items ORDER BY id DESC"

    return db.query(sql)

def get_item(item_id):
    sql= """SELECT items.id,
                   items.name,
                   items.team,
                   items.player_number,
                   items.PPG,
                   items.RPG,
                   items.APG,
                   users.id user_id,
                   users.username
            FROM items, users
            WHERE items.user_id=users.id AND items.id=?"""
    result = db.query(sql,[item_id])
    return result[0] if result else None

def update_item(item_id, name, team, player_number, PPG, RPG, APG,):
    sql = """UPDATE items SET name = ?,
                            team = ?,
                            player_number = ?,
                            PPG = ?,
                            RPG = ?,
                            APG = ?
                        WHERE id = ?"""
    db.execute(sql, [name, team, player_number, PPG, RPG, APG, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def remove_item_classes(item_id):
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql="""SELECT items.id AS item_id, items.name
           FROM items
           LEFT JOIN item_classes ON items.id = item_classes.item_id
           WHERE name LIKE ? OR team LIKE ? OR item_classes.value LIKE ?
           ORDER BY items.id DESC"""
    like= "%" + query + "%"
    return db.query(sql,[like, like, like])
