import sqlite3

connection = sqlite3.connect("initiate_db.bd")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    );
    ''')

def insert_products():
    connection = sqlite3.connect('initiate_db.bd')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Products (title, description, price) VALUES
        ('Product1', 'Описание 1', 100),
        ('Product2', 'Описание 2', 200),
        ('Product3', 'Описание 3', 300),
        ('Product4', 'Описание 4', 400);
        ''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('initiate_db.bd')
    cursor = connection.cursor()
    cursor.execute('SELECT title, description, price FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products

def add_user(username, email, age):
    connection = sqlite3.connect('initiate_db.bd')
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)
    ''', (username, email, age))

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('initiate_db.bd')
    cursor = connection.cursor()

    cursor.execute('''
    SELECT EXISTS(SELECT 1 FROM Users WHERE username = ?)
    ''', (username,))

    result = cursor.fetchone()[0]
    connection.close()

    return result == 1

connection.commit()
connection.close()

