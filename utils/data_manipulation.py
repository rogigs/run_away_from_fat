import sqlite3

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
    PRIMARY KEY (name)
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
            if c.execute("SELECT * FROM user").fetchone():
                c.execute("DELETE FROM user where days>=0")
            c.execute("INSERT INTO user values (?, ?, ?, ?, ?, ?, ?, ?)",
                      [name, who, 0, 0, "", 0, 0, 0])
            conn.commit()
            conn.close()
            return True
        except Exception as ex:
            print(ex)
            return False

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
        kind_to_index = {"speed": 5, "strength": 6, "resistance": 7}
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
            Data.set_next_exercise()
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
            return {"speed": user[5], "strength": user[6], "resistance": user[7]}
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
            return user[2]
        except Exception as ex:
            print(ex)

    @staticmethod
    def set_next_exercise():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            last_kind = c.execute("SELECT * FROM user").fetchone()[4]

            if last_kind == "speed":
                next_kind = "strength"
            elif last_kind == "strength":
                next_kind = "resistance"
            elif last_kind == "resistance":
                next_kind = "marathon"
            else:
                next_kind = "speed"
            c.execute("UPDATE user SET next_ex=?", (next_kind,))
            conn.commit()
            conn.close()
        except Exception as ex:
            print(ex)

    @staticmethod
    def get_next_exercise():
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            next_ex = c.execute("SELECT * FROM user").fetchone()[4]
            conn.commit()
            conn.close()

            return next_ex
        except Exception as ex:
            print(ex)
