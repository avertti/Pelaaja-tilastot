import db

def add_item(name, team, player_number, PPG, RPG, APG, user_id):
    sql = """INSERT INTO items (name, team, player_number, PPG, RPG, APG, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [name, team, player_number, PPG, RPG, APG, user_id])
