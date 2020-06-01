import sqlite3
import bcrypt
conn = sqlite3.connect('lalapass.db')

c = conn.cursor()

def init_db():
    c.execute("""CREATE TABLE IF NOT EXISTS userAccount(
          id integer primary key autoincrement,
          username TEXT NOT NULL,
          hashed_pw CHAR(60) NOT NULL,
          salt CHAR(60) NOT NULL
          )""")
    conn.commit()
    # hashed_password CHAR(60) NOT NULL,
    # salt CHAR(60) NOT NULL


def create_master(username, hashed_pw, salt):
    c.execute("INSERT INTO userAccount (id,username,hashed_pw,salt)VALUES (?,?,?,?)",
              (None, username, hashed_pw, salt,))
    # print("done")
    conn.commit()
    c.execute("SELECT * FROM userAccount")
    print(c.fetchall())
    conn.commit()


def login_verification(username, password):
    c.execute("SELECT * FROM userAccount WHERE username=?", (username,))
    account_details = c.fetchone()
    conn.commit()

    # if bcrypt.checkpw(password.encode('utf8'), account_details[2]):
    #     print("Login Success")
    # else:
    #     print("Failed")
    return bcrypt.checkpw(password.encode('utf8'), account_details[2])


