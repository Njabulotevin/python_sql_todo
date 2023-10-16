from models.database.DatabaseConfig import Database, Column, PrimaryColumn, DataType
from models.user import User
import getpass
import sys
import bcrypt

# Database instance
database = Database()

# Create users table

Id = PrimaryColumn("id", DataType.CHAR(36))
Username = Column("username", DataType.CHAR(255), unique=True, required=True)
Password = Column("password", DataType.CHAR(255))

database.add_columns([Id, Username, Password])


user_1 = User("test_1", "_12345678")
user_2 = User("test_2", "_12345678")
database.create_table("users", database.columns)

# database.insert_into("USERS", column_names=[Id.key, Username.primary, Password.key], column_values=[
#                      user_1.id, user_1.username, user_1.password])


def sign_up():
    username = input("Enter username: ")
    password = getpass.getpass(
        prompt="Enter password: ", stream=sys.stderr)
    new_user = User(username, password)
    database.insert_into("users", column_names=[Id.key, Username.key, Password.key], column_values=[
        str(new_user.id), str(new_user.username), str(new_user.password)])


def sign_in():
    username = input("Enter username: ")
    try:
        res = database.select_by_key("users", "USERNAME", str(username))
        if len(res) != 0:
            password = getpass.getpass(
                prompt="Enter password: ", stream=sys.stderr)
            pw = password.encode("utf-8")
            if bcrypt.checkpw(pw, res[0][-1].encode("utf-8")):
                print("Successfully logged in!")
            else:
                print("Incorrect username or password")

    except Exception as e:
        print(e)
        print("Incorrect username or password")


if __name__ == "__main__":
    sign_in()
    # sign_up()
