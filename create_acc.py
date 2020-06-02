import bcrypt
from database import create_master

def create_acc(username,password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    create_master(username, hashed_password, salt)




