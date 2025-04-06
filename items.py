import db

def add_item(name, team, player_number, PPG, RPG, APG, user_id):
    sql = """INSERT INTO items (name, team, player_number, PPG, RPG, APG, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [name, team, player_number, PPG, RPG, APG, user_id])

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

def find_items(query):
    sql="""SELECT id, name
           FROM items
           WHERE name LIKE ? OR  team LIKE ?
           ORDER BY id DESC"""
    like= "%" + query +"%"
    return db.query(sql,[like, like])
