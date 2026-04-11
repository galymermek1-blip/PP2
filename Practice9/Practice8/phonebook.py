import os
from connect import connect


def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """

    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully")


def run_sql_file(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print(f"{filename} executed successfully")


def upsert_contact(username, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted/updated successfully")


def search_contacts(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\nSearch results:")
    for row in rows:
        print(row)


def insert_many_contacts(usernames, phones):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_many_contacts(%s, %s)", (usernames, phones))

    cur.execute("SELECT * FROM temp_invalid_contacts")
    invalid_rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    print("Bulk insert completed")

    if invalid_rows:
        print("\nIncorrect data:")
        for row in invalid_rows:
            print(row)
    else:
        print("\nNo incorrect data")


def get_contacts_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\nPaginated results:")
    for row in rows:
        print(row)


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted if it existed")


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\nAll contacts:")
    for row in rows:
        print(row)


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Run functions.sql")
        print("3. Run procedures.sql")
        print("4. Insert or update one contact")
        print("5. Search contacts by pattern")
        print("6. Insert many contacts")
        print("7. Show contacts with pagination")
        print("8. Delete contact by username or phone")
        print("9. Show all contacts")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()

        elif choice == "2":
            run_sql_file("functions.sql")

        elif choice == "3":
            run_sql_file("procedures.sql")

        elif choice == "4":
            username = input("Enter username: ")
            phone = input("Enter phone: ")
            upsert_contact(username, phone)

        elif choice == "5":
            pattern = input("Enter pattern: ")
            search_contacts(pattern)

        elif choice == "6":
            n = int(input("How many contacts do you want to add? "))
            usernames = []
            phones = []

            for i in range(n):
                print(f"\nContact {i+1}")
                username = input("Enter username: ")
                phone = input("Enter phone: ")
                usernames.append(username)
                phones.append(phone)

            insert_many_contacts(usernames, phones)

        elif choice == "7":
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))
            get_contacts_paginated(limit, offset)

        elif choice == "8":
            value = input("Enter username or phone to delete: ")
            delete_contact(value)

        elif choice == "9":
            show_all_contacts()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()