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

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items ON DELETE CASCADE,
    title TEXT,
    value TEXT
);
