CREATE TABLE patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    pattern TEXT NOT NULL
);

CREATE TABLE effects (
    id INTEGER PRIMARY KEY,
    breathing INTEGER NOT NULL,
    chasing INTEGER NOT NULL,
    sparkle INTEGER NOT NULL
);