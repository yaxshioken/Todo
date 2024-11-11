from db import Database


class AuthService:
    db=Database()
    def register(self, username, password, email,phone,first_name,last_name):
        if self.db.check_user_exists(username) is None:
            if self.db.create_user(username,password,email,phone,first_name,last_name):
                return True
            else:
                return "Something went wrong"
        else:
            return f"Username already taken{username}"
    def login(self, username, password):
        if self.db.login(username, password):
            return True
        else:
         print("Something went wrong!!!")
