import psycopg2

DB_NAME = "snake_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"  # ← поменяй на свой пароль
DB_HOST = "localhost"
DB_PORT = "5432"


def connect():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        print("Database connection error:", e)
        return None


def init_db():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_player_id(username):
    conn = connect()
    if conn is None:
        return None

    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        player_id = result[0]
    else:
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()

    return player_id


def save_game(username, score, level):
    player_id = get_player_id(username)

    if player_id is None:
        return

    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()


def get_top10():
    conn = connect()
    if conn is None:
        return []

    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result


def get_personal_best(username):
    conn = connect()
    if conn is None:
        return 0

    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        WHERE p.username = %s
    """, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0