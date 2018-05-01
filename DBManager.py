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

	def get_id_by_username(self, username):
		cur = self.conn.cursor()
		cur.execute("SELECT id FROM idmappings WHERE username=%s", (username, ))
		row = cur.fetchone()
		if row is None:
			ret = None
		else:
			ret = int(row[0])

		self.close_cursor(cur)
		return ret

	def check_idmapping(self, user):
		cur = self.conn.cursor()
		username = user["username"]
		id_user = int(user["id"])
		cur.execute("SELECT * FROM idmappings WHERE username=%s", (username,))
		if cur.fetchone() is None:
			cur.execute("INSERT INTO idmappings (username, id) VALUES (%s,%s)", (username, id_user))
		self.close_cursor(cur)

	def test_authorization(self, authorizer_id, authorized_id):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer_id, authorized_id))
		if cur.fetchone() is not None:
			return True
		else:
			return False

	def check_belonging_existence(self, user_id, group_id):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM belongings WHERE group_id=%s AND user_id=%s", (group_id, user_id))
		if cur.fetchone() is None:
			cur.execute("INSERT INTO belongings (group_id, user_id) VALUES (%s,%s)", (group_id, user_id))
		self.close_cursor(cur)

	def check_existence_group(self, group_id):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM belongings WHERE group_id=%s", (group_id, ))
		if cur.fetchone() is None:
			ret = False
		else:
			ret = True
		self.close_cursor(cur)

		return ret

	def get_number_members_group(self, group_id):
		cur = self.conn.cursor()
		cur.execute("SELECT COUNT(*) FROM belongings WHERE group_id=%s", (group_id,))
		ret = int(cur.fetchone()[0])
		self.close_cursor(cur)
		return ret
