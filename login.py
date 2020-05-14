import getpass
import bcrypt
from database import create_master

def login(username,password):
    # username = input("Please enter your username: ")
    # user = input("Username [%s]: " % getpass.getuser())
    # print(getpass.getuser() + user)
    # if not user:
    #     user = getpass.getuser()
    # pprompt = lambda: (getpass.getpass("Please enter your password: "),
    #                    getpass.getpass('Please retype your password: '))
    #
    # p1, p2 = pprompt()

    # while p1 != p2:
    #     print('Passwords do not match. Try again')
    #     p1, p2 = pprompt()

    # hash password
    salt = bcrypt.gensalt()
    # print(salt)
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    # print(hashed_password)
    create_master(username, hashed_password, salt)



#Init Sequence
# print("Hi, welcome to LalaPass :)")

# acc_array = []
# acc_array = login()
# print(len(acc_array))
# print(acc_array[2])

# with open("output/acc.txt", "w", encoding='utf8') as txt_file:
#     for value in acc_array:
#         txt_file.write(str(value) + "\n")
# txt_file.close()
#
# repass = input("Please relogin: ")
# # hashedrepass = bcrypt.hashpw(repass.encode('utf8'), acc_array[2])
# # print(hashedrepass)
# # print(acc_array[1])
# if bcrypt.checkpw(repass.encode('utf8'), acc_array[1]):
#     print("match")
# else:
#     print("does not match")



