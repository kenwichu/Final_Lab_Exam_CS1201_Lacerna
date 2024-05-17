from utils.user import User

class UserManager:
    def __init__(self):
        self.users = {}

    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = User(username, password)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, user in self.users.items():
                file.write(f"{username},{user.password}\n")

    def validate_username(self, username):
        return len(username) >= 4

    def validate_password(self, password):
        return len(password) >= 8

    def register_user(self, username, password):
        if username in self.users:
            return "Username already exists. Please choose another one."
        if not self.validate_username(username):
            return "Username must be at least 4 characters long."
        if not self.validate_password(password):
            return "Password must be at least 8 characters long."
        self.users[username] = User(username, password)
        self.save_users()
        return "Registration successful."

    def login_user(self, username, password):
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            return None
