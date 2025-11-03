import sqlite3
from contextlib import closing

def fetch_person(conn, person_id):
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        "SELECT id, first_name, last_name, age FROM person WHERE id = ?;",
        (person_id,)
    )
    return cur.fetchone()

def fetch_pets_for_person(conn, person_id):
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        """
        SELECT p.name, p.breed, p.age, p.dead
        FROM pet AS p
        JOIN person_pet AS pp ON pp.pet_id = p.id
        WHERE pp.person_id = ?
        ORDER BY p.name;
        """,
        (person_id,)
    )
    return cur.fetchall()

def describe_pet(row):
    name, breed, age, dead = row["name"], row["breed"], row["age"], row["dead"]
    if dead:
        return f"owned {name}, a {breed}, who was {age} years old (deceased)."
    else:
        return f"owns {name}, a {breed}, who is {age} years old."

def main():
    print("Enter a person ID to look up, or -1 to exit.")
    with closing(sqlite3.connect("pets.db")) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        while True:
            try:
                raw = input("Person ID: ").strip()
                if raw == "":
                    continue
                person_id = int(raw)
            except ValueError:
                print("Please enter a valid integer ID or -1 to exit.")
                continue

            if person_id == -1:
                print("Goodbye.")
                break

            person = fetch_person(conn, person_id)
            if not person:
                print(f"Person with ID {person_id} was not found.")
                continue

            full_name = f"{person['first_name']} {person['last_name']}"
            print(f"{full_name}, {person['age']} years old.")

            pets = fetch_pets_for_person(conn, person_id)
            if not pets:
                print(f"{full_name} does not have any pets on record.")
            else:
                for pet in pets:
                    print(f"{full_name} {describe_pet(pet)}")

if __name__ == "__main__":
    main()
