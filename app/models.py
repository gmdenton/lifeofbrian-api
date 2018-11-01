import sqlite3
from constants import *
from sqlite3 import Error

""" Serializable class to hold cheese stock details"""


class Cheese(dict):

    def __init__(self, name, description, size, stock, origin, no_stock_reason):
        self.__setitem__('name', name)
        self.__setitem__('description', description)
        self.__setitem__('size', size)
        self.__setitem__('stock', stock)
        self.__setitem__('origin', origin)
        self.__setitem__('no_stock_reason', no_stock_reason)


""" Serializable class to hold list of cheeses """


class CheeseShop(dict):

    def __init__(self):
        self.items = []
        self.__setitem__("cheeses", self.items)

    def add(self, cheese):
        self.items.append(cheese)

    def remove(self, cheese):
        self.items.append(cheese)


""" Simple class to manage all database calls for cheeseshop table """


class DBCustomer():
    def __init__(self):
        self.error = None
        self.errorCode = None
        self.cheese = None
        self.cheeseshop = CheeseShop()
        self.conn = None
        self.__connect_db()


    def __connect_db(self):

        try:
            self.conn = sqlite3.connect(database_name)
        except Error as e:
            self.error = e

    def insert(self, cheese):
        cur = self.conn.cursor()
        try:
            cur.execute(
                '''INSERT INTO CHEESESHOP (NAME, DESCRIPTION, SIZE, STOCK, ORIGIN, NO_STOCK_REASON) VALUES(?, ?, ?, ?, ?, ?)''',
                (cheese['name'], cheese['description'], cheese['size'], cheese['stock'], cheese['origin'], cheese['no_stock_reason']))
            self.conn.commit()
            self.cheese = cheese
        except Error as e:
            self.error = e
            self.errorCode = 500;
        finally:
            self.conn.close()

    def get(self, name):
        cur = self.conn.cursor()
        try:
            params = (name,)
            cur.execute('SELECT NAME, DESCRIPTION, SIZE, STOCK, ORIGIN, NO_STOCK_REASON FROM CHEESESHOP WHERE NAME = ?', params)
            row = cur.fetchone()
            if row is None:
                self.errorCode = 404
                self.error = '{} is out of stock'.format(name)
            else:
                self.cheese = Cheese(row[0], row[1], row[2], row[3], row[4], row[5])
        except Error as e:
            self.error = e
            self.errorCode = 500;
        finally:
            self.conn.close()

    def read(self):
        cur = self.conn.cursor()
        try:
            cur.execute('SELECT NAME, DESCRIPTION, SIZE, STOCK, ORIGIN, NO_STOCK_REASON FROM CHEESESHOP ORDER BY NAME')
            rows = cur.fetchall()
            if rows is None or len(rows) == 0:
                self.errorCode = 404
                self.error = 'No cheese available. Sorry, I am just going to have to shoot you!'
            else:
                for row in rows:
                    cheese = Cheese(row[0], row[1], row[2], row[3], row[4], row[5])
                    self.cheeseshop.add(cheese)
        except Error as e:
            self.error = e
            self.errorCode = 500;
        finally:
            self.conn.close()

