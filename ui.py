from db import Database
from services import AuthService


class UIMenu:
    auth = AuthService()
    session_user = None

    def welcome(self):
        print("""
        < < < < < < ================== Xush Kelibsiz Todo Proyektiga ============== > > > > > > 
                                    1)Register
                                    2)Login        
        """)
        choice = input("                          Birini tanlang: ")
        match choice:
            case '1':
                self.register()
            case '2':
                self.login()

    def register(self):

        print("< < < < < < ================== Register Menyusi ============== > > > > > > ")
        username = input("Foydalanuvchi nomi: ")
        password = input("Parolni kiriting: ")
        email = input("Email: ")
        phone = input("Telefon Raqam: ")
        first_name = input("Ism : ")
        last_name = input("Familiya: ")
        exit = input("0)Chiqish\n1)Tasqidlash ", )
        if exit == "0":
            print("Chiqilmoqda ... Xayr!")
            return self.welcome()
        else:
            self.auth.register(username, password, email, phone, first_name, last_name)
            print("Registratsiya muvaffaqiyatli yakunlandi!")
            self.welcome()

    def login(self):
        print("< < < < < < ================== Login Menyusi ============== > > > > > > ")

        username = input("Foydalanuvchi nomi: ")
        password = input("Parolni kiriting: ")

        if self.auth.login(username, password):
            self.session_user = username
            print(f"Xush kelibsiz, {username}!")
            return self.user_menu()

        else:
            print("Nimadir xato ketdi! Iltimos, foydalanuvchi nomi yoki parolni tekshirib qayta urinib ko'ring.")
            return self.welcome()

    def user_menu(self):
        print(f"Welcome To My Project ___{self.session_user}")
        print("""
        < < < < < < ================== User Menyusi ============== > > > > > >
         1)Vazifa yaratish
         2)Vazifani yangilash
         3)Vazifani o'chirish
         4)Mening Vazifalarim
         """)
        choice = input("Birini tanlang: ")
        db = Database()
        match choice:
            case '1':
                title = input("Sarlavhani kiriting=>>")
                description = input("Tarif bering=>>")
                status = input("""
                                1) Bajarilishi kerak
                                2) Jarayonda
                                3) Bajarildi
                                Xolatini kiriting=>>""")
                expiration = input("Muddatni kiriting=>>")
                owner=self.session_user
                if db.create_todo(title,owner, description, status, expiration):
                    print("Muvaffaqiyatli Bajarildi!!!")
                    return self.user_menu()
            case '2':
                print(db.all_todo(self.session_user))
                id = input("ID sini kiriting=>>")
                status = input("""              1) Bajarilishi kerak
                                                2) Jarayonda
                                                3) Bajarildi
                                                Xolatini kiriting=>>""")
                if db.update_todo(id, status, self.session_user):
                    print("Muvaffaqiyatli Bajarildi!!!")
                    return self.user_menu()
            case '3':
                print(db.all_todo(self.session_user))
                id = input("ID sini kiriting=>>")
                if db.delete_todo(id):
                    print("Muvaffaqiyatli Bajarildi!!!")
                    return self.user_menu()
            case '4':
                print(db.all_todo(self.session_user))
                exit = input("Exit ", )
                if exit == "Exit":
                    print("Chiqilmoqda ... Xayr!")
                    return self.user_menu()

