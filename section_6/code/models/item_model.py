import sqlite3


class ItemModel:
    _db = 'C:\\Train\\REST_Flask_Python\\data\\data.db'

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def get_item(cls, name):
        connection = sqlite3.connect(cls._db)
        cursor = connection.cursor()
        query = 'SELECT name, price FROM items WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            item = ItemModel(row[0], row[1])
        else:
            item = None

        return item

    @classmethod
    def get_all_items(cls):
        connection = sqlite3.connect(cls._db)
        cursor = connection.cursor()
        query = 'SELECT name, price FROM items ORDER BY name'
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()

        items = []
        for row in rows:
            items.append(ItemModel(row[0], row[1]))

        return items

    def update(self):
        connection = sqlite3.connect(self._db)
        cursor = connection.cursor()
        query = 'UPDATE items SET price = ? WHERE name = ?'
        cursor.execute(query, (self.price, self.name,))
        connection.commit()
        connection.close()

    def add_item(self):
        connection = sqlite3.connect(self._db)
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (self.name, self.price,))
        connection.commit()
        connection.close()

    def delete(self):
        connection = sqlite3.connect(self._db)
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name = ?'
        cursor.execute(query, (self.name,))
        connection.commit()
        connection.close()
