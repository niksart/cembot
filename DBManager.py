import psycopg2 as pg


class DBManager:

	def __init__(self, dbname, user, password, host):
		self.conn = pg.connect(dbname=dbname, user=user, password=password, host=host)

	def get_cursor(self):
		return self.conn.cursor()

	def close_cursor(self, cursor):
		self.conn.commit()  # make changes persistent
		cursor.close()

	def close_connection(self):
		self.conn.commit()  # make changes persistent
		self.conn.close()

	def commit_changes(self):
		self.conn.commit()
