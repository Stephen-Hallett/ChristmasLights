CREATE TABLE Patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    pattern TEXT NOT NULL
);

CREATE TABLE Effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    breathing REAL NOT NULL,
    chasing INTEGER NOT NULL,
    sparkle REAL NOT NULL,
    FOREIGN KEY (id) REFERENCES Patterns(id)
);

INSERT INTO Patterns (name, pattern) VALUES ('Candy Cane', '["#FFFFFF", "#ff2612"]');
INSERT INTO Effects (id, breathing, chasing, sparkle) VALUES (1, 0, 0.5, 1);