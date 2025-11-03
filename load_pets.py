import sqlite3
from contextlib import closing

PERSON_ROWS = [
    (1, 'James', 'Smith', 41),
    (2, 'Diana', 'Greene', 23),
    (3, 'Sara', 'White', 27),
    (4, 'William', 'Gibson', 23),
]

PET_ROWS = [
    (1, 'Rusty', 'Dalmation', 4, 1),
    (2, 'Bella', 'Alaskan Malamute', 3, 0),
    (3, 'Max', 'Cocker Spaniel', 1, 0),
    (4, 'Rocky', 'Beagle', 7, 0),
    (5, 'Rufus', 'Cocker Spaniel', 1, 0),
    (6, 'Spot', 'Bloodhound', 2, 1),
]

PERSON_PET_ROWS = [
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (4, 6),
]

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name  TEXT,
    age INTEGER
);

CREATE TABLE IF NOT EXISTS pet (
    id INTEGER PRIMARY KEY,
    name  TEXT,
    breed TEXT,
    age   INTEGER,
    dead  INTEGER
);

CREATE TABLE IF NOT EXISTS person_pet (
    person_id INTEGER,
    pet_id    INTEGER,
    PRIMARY KEY (person_id, pet_id),
    FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE,
    FOREIGN KEY (pet_id)    REFERENCES pet(id)    ON DELETE CASCADE
);
"""

def main():
    with closing(sqlite3.connect("pets.db")) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        with conn:
            conn.executescript(SCHEMA_SQL)

            # Clear then insert to keep the script idempotent
            conn.execute("DELETE FROM person_pet;")
            conn.execute("DELETE FROM pet;")
            conn.execute("DELETE FROM person;")

            conn.executemany(
                "INSERT INTO person (id, first_name, last_name, age) VALUES (?, ?, ?, ?);",
                PERSON_ROWS
            )
            conn.executemany(
                "INSERT INTO pet (id, name, breed, age, dead) VALUES (?, ?, ?, ?, ?);",
                PET_ROWS
            )
            conn.executemany(
                "INSERT INTO person_pet (person_id, pet_id) VALUES (?, ?);",
                PERSON_PET_ROWS
            )

    print("pets.db created and populated successfully.")

if __name__ == "__main__":
    main()
