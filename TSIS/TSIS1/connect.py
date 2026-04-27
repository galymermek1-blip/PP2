import psycopg2

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="1234",
        host="127.0.0.1",
        port="5432"
    )