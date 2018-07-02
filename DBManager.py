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

	def get_set_users_involved_with_me(self, user_id):
		cur = self.conn.cursor()
		cur.execute("SELECT T.payer, P.payee "
		            "FROM transactions AS T, payees AS P "
		            "WHERE T.id = P.transaction_id "
		            "AND (T.payer = %s OR P.payee = %s)",
		            (user_id, user_id))
		temp = cur.fetchall()
		people = set()
		for (payer, payee) in temp:
			if payer != user_id:
				people.add(payer)
			if payee != user_id:
				people.add(payee)
		self.close_cursor(cur)

		return people

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

	def get_username_by_id(self, id):
		cur = self.conn.cursor()
		cur.execute("SELECT username FROM idmappings WHERE id=%s", (id,))
		row = cur.fetchone()
		if row is None:
			username = None
		else:
			username = row[0]

		self.close_cursor(cur)

		return username

	def update_username_id_mapping(self, user):
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

	def remove_belonging(self, user_id, group_id):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM belongings WHERE group_id=%s AND user_id=%s", (group_id, user_id))
		if not cur.fetchone() is None:
			cur.execute("DELETE FROM belongings WHERE group_id=%s AND user_id=%s", (group_id, user_id))
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

	def get_id_members_by_group(self, group_id):
		cur = self.conn.cursor()
		cur.execute("SELECT user_id FROM belongings WHERE group_id=%s", (group_id,))
		temp = cur.fetchall()
		ret = []
		for (a,) in temp:
			ret.append(a)
		self.close_cursor(cur)
		return ret

	def get_balance(self, user1_id, user2_id):
		cur = self.conn.cursor()
		cur.execute("SELECT T.payer, P.payee, T.amount "
		            "FROM transactions AS T, payees AS P "
		            "WHERE T.id = P.transaction_id "
		            "AND ((T.payer = %s AND P.payee = %s) OR (T.payer = %s AND P.payee = %s))",
		            (user1_id, user2_id, user2_id, user1_id))
		temp = cur.fetchall()
		total_amount = 0
		for (payer, payee, amount) in temp:
			if payer == user1_id and payee == user2_id:
				total_amount = total_amount + amount
			if payer == user2_id and payee == user1_id:
				total_amount = total_amount - amount
		self.close_cursor(cur)

		return total_amount/100
