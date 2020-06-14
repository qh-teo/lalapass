import sqlite3
import bcrypt
conn = sqlite3.connect('lalapass.db')
# https://www.tutorialspoint.com/sqlite/sqlite_update_query.htm
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
              id INTEGER primary key autoincrement,
              user_id INTEGER,
              account_user TEXT NOT NULL,
              account_pw CHAR(60) NOT NULL,
              account_type TEXT NOT NULL,
              FOREIGN KEY(user_id) REFERENCES userAccount(id)
              )""")
    conn.commit()
  

def create_master(username, hashed_pw, salt):
    c.execute("INSERT INTO userAccount (id,username,hashed_pw,salt)VALUES (?,?,?,?)",
              (None, username, hashed_pw, salt,))
    conn.commit()
    c.execute("SELECT * FROM userAccount")
    # print(c.fetchall())
    conn.commit()

def login_verification(username, password):
    c.execute("SELECT * FROM userAccount WHERE username=?", (username,))
    account_details = c.fetchone()
    conn.commit()

    verification = bcrypt.checkpw(password.encode('utf8'), account_details[2])

    if verification is True:
        return verification, account_details[0], account_details[3]
    else:
        return verification


def create_profile(user_id, username, password, profile):
    c.execute("INSERT INTO accounts (id,user_id,account_user,account_pw,account_type)VALUES (?,?,?,?,?)",
              (None,user_id, username, password, profile,))
    conn.commit()


def retrieve_profile(user_id):
    c.execute("SELECT id,account_user,account_pw,account_type FROM accounts WHERE user_id=?", (user_id,))
    account_details = c.fetchall()
    conn.commit()
    return account_details


def update_profile(profileId, username, password, profile_type):
    c.execute("UPDATE accounts SET account_user=?, account_pw=?, account_type=? WHERE ID=?",
              (username, password, profile_type, profileId,))
    conn.commit()


def delete_profile(profileId):
    # """DELETE from SqliteDb_developers where id = ?"""
    c.execute("DELETE from accounts WHERE ID=?", (profileId,))
    conn.commit()

