import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS user (
    person char,
    days integer,
    coins integer,
    speed integer,
    stamina integer,
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
            c.execute("INSERT INTO user values (?, ?, ?, ?, ?, ?)", [who, 0, 0, 0, 0, 0])
            conn.commit()
            conn.close()
            return True
        except Exception as ex:
            print(ex)
