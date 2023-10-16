import uuid
import bcrypt

salt = bcrypt.gensalt()


class User:
    def __init__(self, username: str, password: str) -> None:
        self.id = uuid.uuid4()
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), salt).decode("utf-8")

    def get_user(self):
        return (self.id, self.username, self.password)


class Users:
    list_of_users: User = []

    def __init__(self) -> None:
        # get users from
        pass

    def add_user(self, user: User):
        self.list_of_users.append(user)

    def get_users(self):
        return self.list_of_users


users = Users()
# users.add_user(User("test_1", "122345"))

print(users.get_users())
