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


connection.commit()
connection.close()

