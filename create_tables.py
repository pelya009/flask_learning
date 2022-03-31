import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_table)

insert_query = 'INSERT INTO users VALUES (NULL, ?, ?)'

users = [
    ('admin', 'admin'),
    ('roman', 'pelya'),
    ('taya', 'yagoza')
]

cursor.executemany(insert_query, users)

create_table = 'CREATE TABLE IF NOT EXISTS items (name text, price real)'
cursor.execute(create_table)

insert_query = 'INSERT INTO items VALUES (?, ?)'

items = [
    ('ferrari', 500.0),
    ('porshe', 367.7),
    ('mclaren', 124.45)
]

cursor.executemany(insert_query, items)

connection.commit()
connection.close()