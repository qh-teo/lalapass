import sqlite3
import bcrypt
conn = sqlite3.connect('lalapass.db')

c = conn.cursor()

def init_db():
    c.execute("""CREATE TABLE IF NOT EXISTS userAccount(
          id INTEGER primary key autoincrement,
          username  TEXT NOT NULL,
          hashed_pw CHAR(60) NOT NULL,
          salt CHAR(60) NOT NULL
          )""")
    conn.commit()

    c.execute("""CREATE TABLE IF NOT EXISTS accounts(
              id INTEGER primary key  autoincrement,
              account_user TEXT NOT NULL,
              account_pw TEXT NOT NULL,
              account_type TEXT NOT NULL
              )""")
        # user_id INTEGER,
        # FOREIGN KEY(user_id) REFERENCES userAccount(id)
    conn.commit()


def create_master(username, hashed_pw, salt):
    c.execute("INSERT INTO userAccount (id,username,hashed_pw,salt)VALUES (?,?,?,?)",
              (None, username, hashed_pw, salt,))
    conn.commit()
    c.execute("SELECT * FROM userAccount")
    print(c.fetchall())
    conn.commit()


def login_verification(username, password):
    c.execute("SELECT * FROM userAccount WHERE username=?", (username,))
    account_details = c.fetchone()
    conn.commit()

    return bcrypt.checkpw(password.encode('utf8'), account_details[2])


