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
		try:
			username = user["username"]
		except KeyError:
			return

		cur = self.conn.cursor()
		id_user = int(user["id"])
		cur.execute("SELECT id, username FROM idmappings WHERE id=%s", (id_user,))
		occurrence = cur.fetchone()
		if occurrence is None:
			cur.execute("INSERT INTO idmappings (username, id) VALUES (%s,%s)", (username, id_user))
		else:
			(id_db, username_db) = occurrence
			if username_db != username:
				cur.execute("UPDATE idmappings SET username=%s WHERE id=%s", (username, id_user))
		self.close_cursor(cur)

	def test_authorization(self, authorizer_id, authorized_id):
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer_id, authorized_id))
		if cur.fetchone() is not None:
			return True
		else:
			return False

	def update_groupname_id_mappings(self, group_id, group_name):
		cur = self.conn.cursor()
		cur.execute("SELECT name FROM groupmappings WHERE id=%s", (group_id,))
		occurrence = cur.fetchone()
		if occurrence is None:
			cur.execute("INSERT INTO groupmappings (id, name) VALUES (%s,%s)", (group_id, group_name))
		else: #controllo che il nome settato sia uguale al group name, se no lo aggiorno
			(name_db,) = occurrence
			if name_db != group_name:
				cur.execute("UPDATE groupmappings SET name=%s WHERE id=%s", (group_name, group_id))
		self.close_cursor(cur)

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
		cur.execute("SELECT T.id, T.payer, P.payee, T.amount, group_id "
		            "FROM transactions AS T, payees AS P "
		            "WHERE T.id = P.transaction_id AND "
		                "((T.payer = %s AND P.payee = %s) OR (T.payer = %s AND P.payee = %s));",
		            (user1_id, user2_id, user2_id, user1_id))
		temp = cur.fetchall()
		total_amount = 0
		for (transaction_id, payer, payee, amount, group_id) in temp:
			if group_id is not None:
				cur.execute("SELECT COUNT(*) FROM payees WHERE transaction_id=%s", (transaction_id,))
				(number_payees,) = cur.fetchone()
				amount = amount / number_payees

			if payer == user1_id and payee == user2_id:
				total_amount = total_amount + amount
			if payer == user2_id and payee == user1_id:
				total_amount = total_amount - amount

		self.close_cursor(cur)

		return total_amount/100

	# get last n charges over the user passed
	# returns a list of tuples (payer username or id, amount, description)
	def get_last_n_charges(self, user_id, n):
		charges_of_individuals = []
		cur = self.conn.cursor()
		cur.execute("SELECT payer, amount, description FROM payees AS P, transactions AS T "
		            "WHERE P.transaction_id=T.id AND payee=%s AND group_id IS NULL AND amount>0 "
		            "ORDER BY T.time DESC "
		            "LIMIT %s",
		            (user_id, n))
		temp = cur.fetchall()

		for (payer_id, amount, description) in temp:
			username = self.get_username_by_id(payer_id)
			charges_of_individuals.append((str(payer_id) if username is None else username, amount / 100, description))

		charges_of_groups= []
		cur.execute("SELECT T.payer, T.amount, description, GM.name, T.id "
		            "FROM transactions AS T, payees AS P, groupmappings AS GM "
		            "WHERE T.id = P.transaction_id AND GM.id=group_id AND P.payee = %s AND group_id IS NOT NULL AND T.payer != %s "
		            "ORDER BY T.time DESC "
		            "LIMIT %s",
		            (user_id, user_id, n))
		temp = cur.fetchall()

		for (payer_id, amount, description, group_name, transaction_id) in temp:
			username = self.get_username_by_id(payer_id)
			cur.execute("SELECT COUNT(*) FROM payees WHERE transaction_id=%s", (transaction_id,))
			(number_payees, ) = cur.fetchone()
			charges_of_groups.append((str(payer_id) if username is None else username, (amount/number_payees)/100, description, group_name))

		self.close_cursor(cur)

		return (charges_of_individuals, charges_of_groups)

	# get last n loans over the user passed
	def get_last_n_loans(self, user_id, n):
			loans_of_individuals = []
			cur = self.conn.cursor()
			cur.execute("SELECT payee, amount, description FROM payees AS P, transactions AS T "
			            "WHERE P.transaction_id=T.id AND payer=%s AND group_id IS NULL AND amount>0 "
			            "ORDER BY T.time DESC "
			            "LIMIT %s",
			            (user_id, n))
			temp = cur.fetchall()

			for (payee_id, amount, description) in temp:
				username = self.get_username_by_id(payee_id)
				loans_of_individuals.append((str(payee_id) if username is None else username, amount / 100, description))

			loans_of_groups = []
			cur.execute("SELECT T.amount, description, GM.name "
			            "FROM transactions AS T, groupmappings AS GM "
			            "WHERE GM.id=group_id AND T.payer = %s AND group_id IS NOT NULL "
			            "ORDER BY T.time DESC "
			            "LIMIT %s",
			            (user_id, n))
			temp = cur.fetchall()
			for (amount, description, group_name) in temp:
				loans_of_groups.append((group_name, amount/100, description))
			self.close_cursor(cur)

			return (loans_of_individuals, loans_of_groups)

	# get last n loans over the user passed
	# returns a list of tuples (payer username or id, amount, description)
	def get_last_n_group_expenses(self, group_id, n):
		ret = []
		cur = self.conn.cursor()
		cur.execute("SELECT payer, amount, description "
		            "FROM transactions "
		            "WHERE group_id=%s AND amount>0 "
		            "ORDER BY time DESC "
		            "LIMIT %s",
		            (group_id, n))
		temp = cur.fetchall()

		for (payer_id, amount, description) in temp:
			username = self.get_username_by_id(payer_id)
			ret.append((str(payer_id) if username is None else username, amount / 100, description))
		self.close_cursor(cur)

		return ret
