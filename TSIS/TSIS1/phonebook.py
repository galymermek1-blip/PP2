import json
import csv
from connect import connect


# ---------- ADD CONTACT ----------
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    g = cur.fetchone()

    if g:
        gid = g[0]
    else:
        cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group,))
        gid = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name,email,birthday,group_id)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (name) DO NOTHING
    """, (name,email,birthday,gid))

    conn.commit()
    conn.close()


# ---------- ADD PHONE ----------
def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s,%s,%s)", (name,phone,ptype))
    conn.commit()
    conn.close()


# ---------- MOVE GROUP ----------
def move_group():
    name = input("Name: ")
    group = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s,%s)", (name,group))
    conn.commit()
    conn.close()


# ---------- SEARCH ----------
def search():
    q = input("Search: ")
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall():
        print(row)

    conn.close()


# ---------- FILTER ----------
def filter_group():
    g = input("Group: ")
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name,c.email FROM contacts c
        JOIN groups g ON c.group_id=g.id
        WHERE g.name=%s
    """, (g,))

    print(cur.fetchall())
    conn.close()


# ---------- SORT ----------
def sort_contacts():
    field = input("Sort by (name/birthday/date): ")

    if field == "name":
        order = "name"
    elif field == "birthday":
        order = "birthday"
    else:
        order = "created_at"

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"SELECT name,email,birthday FROM contacts ORDER BY {order}")
    print(cur.fetchall())

    conn.close()


# ---------- PAGINATION ----------
def paginate():
    limit = 3
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        cur.execute("""
            SELECT name,email FROM contacts
            ORDER BY name
            LIMIT %s OFFSET %s
        """, (limit,offset))

        print(cur.fetchall())

        cmd = input("next/prev/quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset-limit)
        else:
            break

    conn.close()


# ---------- EXPORT JSON ----------
def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name,c.email,g.name,p.phone,p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json","w") as f:
        json.dump(data,f,indent=4)

    conn.close()


# ---------- IMPORT JSON ----------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    conn = connect()
    cur = conn.cursor()

    for row in data:
        name,email,group,phone,ptype = row

        cur.execute("""
            INSERT INTO contacts(name,email)
            VALUES (%s,%s)
            ON CONFLICT(name) DO UPDATE SET email=EXCLUDED.email
        """,(name,email))

        cur.execute("CALL move_to_group(%s,%s)", (name,group))

        if phone:
            cur.execute("CALL add_phone(%s,%s,%s)", (name,phone,ptype))

    conn.commit()
    conn.close()


# ---------- CSV IMPORT ----------
def import_csv():
    with open("contacts.csv") as f:
        reader = csv.DictReader(f)

        conn = connect()
        cur = conn.cursor()

        for row in reader:
            name = row["name"]
            email = row["email"]
            group = row["group"]
            phone = row["phone"]
            ptype = row["type"]

            cur.execute("""
                INSERT INTO contacts(name,email)
                VALUES (%s,%s)
                ON CONFLICT DO NOTHING
            """,(name,email))

            cur.execute("CALL move_to_group(%s,%s)", (name,group))
            cur.execute("CALL add_phone(%s,%s,%s)", (name,phone,ptype))

        conn.commit()
        conn.close()


# ---------- MENU ----------
def menu():
    while True:
        print("""
1 Add contact
2 Add phone
3 Move group
4 Search
5 Filter by group
6 Sort
7 Pagination
8 Export JSON
9 Import JSON
10 Import CSV
0 Exit
        """)

        c = input(">> ")

        if c=="1": add_contact()
        elif c=="2": add_phone()
        elif c=="3": move_group()
        elif c=="4": search()
        elif c=="5": filter_group()
        elif c=="6": sort_contacts()
        elif c=="7": paginate()
        elif c=="8": export_json()
        elif c=="9": import_json()
        elif c=="10": import_csv()
        else: break


if __name__ == "__main__":
    menu()