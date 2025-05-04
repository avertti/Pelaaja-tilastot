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

def add_comment(item_id, user_id, comment):
    sql = """INSERT INTO comments (item_id, user_id, text) VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql = """SELECT comments.text, users.id AS user_id,            users.username
           FROM comments, users
           WHERE comments.item_id = ? AND comments.user_id = users.id
           ORDER BY comments.id DESC"""
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
    remove_comments(item_id)
    remove_item_classes(item_id)
    remove_ratings(item_id)
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def remove_item_classes(item_id):
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

def remove_comments(item_id):
    sql = "DELETE FROM comments WHERE item_id = ?"
    db.execute(sql, [item_id])

def remove_ratings(item_id):
    sql = "DELETE FROM ratings WHERE item_id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql="""SELECT items.id AS item_id, items.name
           FROM items
           LEFT JOIN item_classes ON items.id = item_classes.item_id
           WHERE name LIKE ? OR team LIKE ? OR item_classes.value LIKE ?
           ORDER BY items.id DESC"""
    like= "%" + query + "%"
    return db.query(sql,[like, like, like])

def get_rankings():
    sql = """SELECT items.id, items.name, ROUND(AVG(ratings.rating),2) as avg_rating
    FROM itemS JOIN ratings ON items.id = ratings.item_id
    GROUP BY items.id ORDER BY avg_rating DESC"""
    rankings = db.query(sql)

    for ranking in rankings:
        sql_insert = """INSERT INTO rankings (player_id,avg_rating)
        VALUES (?,?)"""
    return rankings

def get_avg_rating(item_id):
    result = db.query("""
        SELECT ROUND(AVG(rating), 2) AS avg_rating
        FROM ratings
        WHERE item_id = ?
    """, (item_id,))

    if result:
        avg_rating = result[0]["avg_rating"]
        return avg_rating if avg_rating else "Ei arvioita"
    return "Ei arvioita"
