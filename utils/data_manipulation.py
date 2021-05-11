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
        kind_to_index = {"speed": 3, "strength": 4, "resistance": 5}
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user")
            if c.fetchone()[kind_to_index[kind]] <= 90:
                c.execute(f"UPDATE user set {kind} = {kind} + {num} WHERE days >= 0")
            conn.commit()
            conn.close()
            return
        except Exception as ex:
            print(ex)

    @staticmethod
    def increase_day():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user")
            c.execute(f"UPDATE user set days = days + 1 WHERE days >= 0")
            conn.commit()
            conn.close()
            return
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_status():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user")
            user = c.fetchone()
            conn.commit()
            conn.close()
            return {"speed": user[3], "strength": user[4], "resistance": user[5]}
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_day():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user")
            user = c.fetchone()
            conn.commit()
            conn.close()
            return user[1]
        except Exception as ex:
            print(ex)