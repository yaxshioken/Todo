import os
from ctypes.wintypes import tagMSG
from os.path import curdir
from venv import create

from dotenv import load_dotenv
from utils import make_password, match_password

load_dotenv()
import psycopg2


class Database:

    def __init__(self):
        self.db = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"),
                                   user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), )
        self.db.autocommit = True
        self.cursor = self.db.cursor()

    def create_todo_table(self):
        create_todo_sql = """
        CREATE TABLE IF NOT EXISTS todo(
        id serial PRIMARY KEY,
        title varchar(255) unique not null,
        owner varchar(255) references users(username) on delete cascade,
        description text,
        status varchar(255) not null,
        expiration date
        );
        """

    def create_user_table(self):
        create_user_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(255) NOT NULL ,
            first_name VARCHAR(255) ,
            last_name VARCHAR(255)
            );
            
            """
        self.cursor.execute(create_user_table_sql)
        self.db.commit()

    def check_user_exists(self, username):
        check_username_sql = """
        select *from users where username = %s;
        """
        self.cursor.execute(check_username_sql, (username,))
        result = self.cursor.fetchall()
        if result is None:
            return True

    def create_user(self, username, password, email, phone, first_name, last_name):

        try:
            insert_user_sql = """
            INSERT INTO users (username, password, email, phone, first_name, last_name) values (%s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(insert_user_sql, (username, password, email, phone, first_name, last_name))
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def login(self, username, password):
        login_sql = """
        select password from users where username = %s;
        """
        self.cursor.execute(login_sql, (username,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def create_todo(self, title, description, owner, status, expiration):
        create_todo_sql = """
        insert into todo (title, owner, description, status, expiration) values (%s,%s,%s,%s,%s)"""
        match status:
            case "1":
                status = "Bajarilishi kerak"
            case "2":
                status = "Jarayonda"
            case "3":
                status = "Bajarildi"
        self.cursor.execute(create_todo_sql, (title, description, owner, status, expiration))
        self.db.commit()
        return True

    def all_todo(self, username):
        all_todo_sql = """select * from todo where  owner=%s"""
        self.cursor.execute(all_todo_sql, (username,))
        result = self.cursor.fetchall()
        return result

    def update_todo(self, id, val, owner):
        update_todo_sql = """
        UPDATE todo SET status=%s WHERE id=%s and owner %s;"""
        if self.cursor.execute(update_todo_sql, (id, val, owner)):
            self.db.commit()
            return True
        else:
            return "Something Went Wrong"

    def delete_todo(self, id):
        delete_todo_sql = """
       DELETE FROM todo WHERE id=%s;
       """
        if self.cursor.execute(delete_todo_sql, (id,)):
            self.db.commit()
            return True
        else:
            return "Something Went Wrong"
