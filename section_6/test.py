import sqlite3

connection = sqlite3.connect('data.db')

# cursor can run query and store result
cursor = connection.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text)'
cursor.execute(create_table)

user = (1, 'jose', 'pwd')
insert_query = 'INSERT INTO users VALUES (?, ?, ?)'
cursor.execute(insert_query, user)

users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'sumpwd'),
    (4, 'kirk', 'pwd')
]

cursor.executemany(insert_query, users)

select_query = 'SELECT * FROM users'
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
