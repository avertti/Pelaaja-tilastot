CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    team TEXT,
    player_number INTEGER,
    PPG REAL,
    RPG REAL,
    APG REAL,
    user_id INTEGER REFERENCES users
);
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items ON DELETE CASCADE,
    user_id INTEGER REFERENCES users,
    rating INTEGER
);
CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items ON DELETE CASCADE,
    title TEXT,
    value TEXT
);
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items ON DELETE CASCADE,
    user_id INTEGER REFERENCES users,
    text TEXT
);
CREATE TABLE rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT
    player_id INTEGER,
    avg_rating REAL,
    rankings_date TIMESTAMP DEFAULT CURRENT_ITEMSTAMP,
    FOREIGN KEY (player_id) REFERENCES items(id)
);
