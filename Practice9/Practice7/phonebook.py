import psycopg2
import csv

def connect():
    return psycopg2.connect(
        host="localhost",
        database="suppliers",
        user="postgres",
        password="0311"
    )


def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql)
        conn.commit()

        cur.close()
        conn.close()
        print("Table created")

    except Exception as e:
        print("Error:", e)


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    sql = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (username, phone))
        conn.commit()

        cur.close()
        conn.close()
        print("Inserted successfully")

    except Exception as e:
        print("Error:", e)


def insert_from_csv(filename):
    sql = """
    INSERT INTO phonebook (username, phone)
    VALUES (%s, %s)
    ON CONFLICT (phone) DO NOTHING
    """
    try:
        conn = connect()
        cur = conn.cursor()

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cur.execute(sql, (row[0], row[1]))

        conn.commit()
        cur.close()
        conn.close()
        print("CSV inserted successfully")

    except Exception as e:
        print("Error:", e)


def query_all():
    sql = "SELECT * FROM phonebook ORDER BY id"
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql)
        rows = cur.fetchall()

        if not rows:
            print("Phonebook is empty")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def query_by_username(username):
    sql = """
    SELECT * FROM phonebook
    WHERE username ILIKE %s
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (f"%{username}%",))
        rows = cur.fetchall()

        if not rows:
            print("No contacts found")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def query_by_phone(phone):
    sql = """
    SELECT * FROM phonebook
    WHERE phone LIKE %s
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (f"%{phone}%",))
        rows = cur.fetchall()

        if not rows:
            print("No contacts found")
        else:
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def update_username(old_username, new_username):
    sql = """
    UPDATE phonebook
    SET username = %s
    WHERE username = %s
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (new_username, old_username))
        conn.commit()

        print("Updated rows:", cur.rowcount)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def update_phone(username, new_phone):
    sql = """
    UPDATE phonebook
    SET phone = %s
    WHERE username = %s
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (new_phone, username))
        conn.commit()

        print("Updated rows:", cur.rowcount)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def delete_by_username(username):
    sql = """
    DELETE FROM phonebook
    WHERE username = %s
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (username,))
        conn.commit()

        print("Deleted rows:", cur.rowcount)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def delete_by_phone(phone):
    sql = """
    DELETE FROM phonebook
    WHERE phone = %s
    """
    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(sql, (phone,))
        conn.commit()

        print("Deleted rows:", cur.rowcount)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Show all contacts")
        print("5. Search by username")
        print("6. Search by phone")
        print("7. Update username")
        print("8. Update phone")
        print("9. Delete by username")
        print("10. Delete by phone")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            create_table()

        elif choice == "2":
            insert_from_console()

        elif choice == "3":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)

        elif choice == "4":
            query_all()

        elif choice == "5":
            username = input("Enter username to search: ")
            query_by_username(username)

        elif choice == "6":
            phone = input("Enter phone to search: ")
            query_by_phone(phone)

        elif choice == "7":
            old_username = input("Enter old username: ")
            new_username = input("Enter new username: ")
            update_username(old_username, new_username)

        elif choice == "8":
            username = input("Enter username: ")
            new_phone = input("Enter new phone: ")
            update_phone(username, new_phone)

        elif choice == "9":
            username = input("Enter username to delete: ")
            delete_by_username(username)

        elif choice == "10":
            phone = input("Enter phone to delete: ")
            delete_by_phone(phone)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()