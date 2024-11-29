CREATE TABLE Patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    pattern TEXT NOT NULL,
    active INTEGER NOT NULL
);

CREATE UNIQUE INDEX one_active_pattern ON Patterns(active) WHERE active = 1;

CREATE TABLE Effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breathing REAL NOT NULL,
    chasing REAL NOT NULL,
    sparkle INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES Patterns(id)
);

INSERT INTO Patterns (name, pattern, active) VALUES ('Candy Cane', '["#FFFFFF", "#ff2612"]', 1);
INSERT INTO Effects (id, breathing, chasing, sparkle) VALUES (1, 0, 0.5, 1);