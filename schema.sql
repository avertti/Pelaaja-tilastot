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
