import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS user (
    person char,
    days integer,
    coins integer,
    speed integer,
    strength integer,
    resistance integer,
    PRIMARY KEY (person)
)""")
conn.commit()
conn.close()


class Data:
    def __init__(self):
        pass

    @staticmethod
    def has_save():
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user")
        if c.fetchone():
            conn.close()
            return True
        conn.close()
        return False

    @staticmethod
    def create_new_person(who):
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            if c.execute("SELECT * FROM user").fetchone():
                c.execute("DELETE FROM user where days>=0")
            c.execute("INSERT INTO user values (?, ?, ?, ?, ?, ?)",
                      [who, 0, 0, 0, 0, 0])
            conn.commit()
            conn.close()
            return True
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_character():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM user")
            rows = c.fetchone()
            conn.commit()
            conn.close()
            return rows
        except Exception as ex:
            print(ex)

    @staticmethod
    def increase_status(num, kind):
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"UPDATE user set {kind} = {kind} + {num} WHERE days >= 0")
            conn.commit()
            conn.close()
            return
        except Exception as ex:
            print(ex)