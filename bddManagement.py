import sqlite3
import sys

BOOL_NONE = 2
BOOL_TRUE = 1
BOOL_FALSE = 0


class DatabaseManager:

	def __init__(self, database="default.db"):
		"""Init the database, create a file if it don't exist and initialize the table if needed"""
		self.Conn = sqlite3.connect(database)
		self.DbCursor = self.Conn.cursor()
		self.DbCursor.execute('''create table if not exists Toys (id INT PRIMARY KEY, toy_name TEXT, toy_size INTEGER,
													toy_type INTEGER, color TEXT, firmness INTEGER, cumtube INTEGER, suction_cup INTEGER, flop INTEGER,
													description TEXT, update_time FLOAT)''')
		self.DbCursor.execute('''create table if not exists Filters (user_id INT PRIMARY KEY, filter_name TEXT, toy_name TEXT, 
													toy_size INTEGER, size_comparator INTEGER, toy_type INTEGER, color TEXT, firmness INTEGER, 
													cumtube INTEGER, suction_cup INTEGER, flop INTEGER, description TEXT,
													PRIMARY KEY(user_id, filter_name))''')
		self.Conn.commit()

	def get_toys(self):
		"""Retrieve all toys from the database"""
		self.DbCursor.execute('''SELECT * FROM Toys''')
		return self.DbCursor.fetchall()

	def get_filters(self):
		"""Retrieve all the filters from the database"""
		self.DbCursor.execute('''SELECT * FROM Filters''')
		return self.DbCursor.fetchall()

	def set_toy(self, toys):
		"""Remove all toy and set add multiple toy"""
		self.DbCursor.execute('''DELETE from Toys''')
		self.Conn.commit()
		self.DbCursor.executemany('''INSERT INTO Toys VALUES (?,?,?,?,?,?,?,?,?,?,?)''', toys)
		self.Conn.commit()

	def add_filter(self, filter_data):
		"""Remove all toy and set add multiple toy"""
		self.DbCursor.execute('''INSERT INTO Filters VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', filter_data)
		self.Conn.commit()

	def remove_filter(self, user_id, filter_name):
		"""Remove a filter with it key (user, name) in the database"""
		self.DbCursor.execute('''DELETE FROM Filters WHERE user_id == ? and filter_name == ? ''', (user_id, filter_name))
		self.Conn.commit()
