import sqlite3

import config

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS user (
    name text,
    person char,
    days integer,
    coins integer,
    next_ex text,
    speed integer,
    strength integer,
    resistance integer,
    PRIMARY KEY (name, days)
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
    def create_new_person(who, name):
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            if not c.execute("SELECT * FROM user WHERE name=? AND days=0", (name,)).fetchone():
                c.execute("INSERT INTO user values (?, ?, ?, ?, ?, ?, ?, ?)",
                          [name, who, 0, 0, 'speed', 0, 0, 0])
                config.USERNAME = name
            conn.commit()
            conn.close()
            return True
        except Exception as ex:
            print(ex, "create_new_person")
            return False

    @staticmethod
    def get_character():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE name=?", (config.USERNAME,))
            rows = c.fetchone()
            conn.commit()
            conn.close()
            return rows
        except Exception as ex:
            print(ex, "get_character")

    @staticmethod
    def increase_status(num, kind):
        kind_to_index = {"speed": 5, "strength": 6, "resistance": 7}
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user WHERE name=?", (config.USERNAME,))
            if c.fetchone()[kind_to_index[kind]] <= 90:
                c.execute(f"UPDATE user set {kind} = {kind} + {num} WHERE name=?", (config.USERNAME,))
            conn.commit()
            conn.close()
            return
        except Exception as ex:
            print(ex, "increase_status")

    @staticmethod
    def increase_day():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"UPDATE user set days = days + 1 WHERE name=?", (config.USERNAME,))
            conn.commit()
            conn.close()
            Data.set_next_exercise()
            return
        except Exception as ex:
            print(ex, "increase_day")

    @staticmethod
    def get_status():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user WHERE name=?", (config.USERNAME,))
            user = c.fetchone()
            conn.commit()
            conn.close()
            return {"speed": user[5], "strength": user[6], "resistance": user[7]}
        except Exception as ex:
            print(ex, "get_status")

    @staticmethod
    def get_day():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute(f"SELECT * FROM user WHERE name=?", (config.USERNAME,))
            user = c.fetchone()
            conn.commit()
            conn.close()
            return user[2]
        except Exception as ex:
            print(ex, "get_day")

    @staticmethod
    def set_next_exercise():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            last_kind = c.execute("SELECT * FROM user WHERE name=?", (config.USERNAME,)).fetchone()[4]

            if last_kind == "speed":
                next_kind = "strength"
            elif last_kind == "strength":
                next_kind = "resistance"
            elif last_kind == "resistance":
                next_kind = "marathon"
            else:
                next_kind = "speed"
            c.execute("UPDATE user SET next_ex=? WHERE name=?", (next_kind, config.USERNAME))
            conn.commit()
            conn.close()
        except Exception as ex:
            print(ex, "set_next_exercise")

    @staticmethod
    def get_next_exercise():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            next_ex = c.execute("SELECT * FROM user WHERE name=?", (config.USERNAME,)).fetchone()[4]
            conn.commit()
            conn.close()

            return next_ex
        except Exception as ex:
            print(ex, "get_next_exercise")

    @staticmethod
    def get_saves():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            saves = c.execute("SELECT * FROM user").fetchall()[:5]
            conn.commit()
            conn.close()
            return saves
        except Exception as ex:
            print(ex, "get_saves")
