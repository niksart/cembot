#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot
import telepot.routing
import telepot.loop
import time
import sys
import os
import DBManager


def send_markdown_message(bot, chat_id, text):
	bot.sendMessage(chat_id, text, parse_mode="Markdown")


def authorize(bot, user, chat, args):
	authorizer_id = int(user["id"])

	if len(args) != 1:
		send_markdown_message(bot, chat["id"], helpers[authorize])
		return

	authorized_username = args[0]
	authorized_id = dbman.get_id_by_username(authorized_username)
	if authorized_id is None:
		send_markdown_message(bot, chat["id"], "The user @%s that you want to authorize is not registered on our system" % authorized_username)
		return

	print("%s: 'please authorize this user: %s'" % (authorizer_id, authorized_id))

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer_id, authorized_id))
	if cur.fetchone() is not None:
		bot.sendMessage(chat["id"], "You have already authorized this user.")
	else:
		cur.execute("INSERT INTO authorizations (authorizer, authorized) VALUES (%s, %s)", (authorizer_id, authorized_id))
		bot.sendMessage(chat["id"], "User @%s has been authorized." % authorized_username)
	dbman.close_cursor(cur)


def deauthorize(bot, user, chat, args):
	deauthorizer_id = int(user["id"])

	if len(args) != 1:
		send_markdown_message(bot, chat["id"], helpers[deauthorize])
		return

	deauthorized_username = args[0]
	deauthorized_id = dbman.get_id_by_username(deauthorized_username)
	if deauthorized_id is None:
		send_markdown_message(bot, chat["id"], "The user @%s that you want to deauthorize is not registered on our system" % deauthorized_username)
		return

	print("%s: 'please deauthorize this user: %s'" % (deauthorizer_id, deauthorized_id))

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer_id, deauthorized_id))
	if cur.fetchone() is None:
		bot.sendMessage(chat["id"], "You have not already authorized this user. You can't deauthorize it.")
	else:
		cur.execute("DELETE FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer_id, deauthorized_id))
		bot.sendMessage(chat["id"], "User @%s has been deauthorized." % deauthorized_username)
	dbman.close_cursor(cur)


def given(bot, user, chat, args):
	payer_id = int(user["id"])

	if len(args) != 2:
		send_markdown_message(bot, chat["id"], helpers[given])
		return

	try:
		amountstr = args[0].replace(',', '.').replace('€', '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], "Amount of money not valid.")
		return

	payee_username = args[1]
	payee_id = dbman.get_id_by_username(payee_username)
	if payee_id is None:
		send_markdown_message(bot, chat["id"], "The user @%s that you want to add as a payee is not registered on our system" % payee_username)
		return

	if not dbman.test_authorization(payee_id, payer_id):  # if payee has not authorized the payer exit
		send_markdown_message(bot, chat["id"], "The user @%s has not authorized you for charging expenses" % payee_username)
		return

	try:
		cur = dbman.get_cursor()
		cur.execute("INSERT INTO transactions (payer, amount, time) VALUES (%s, %s, %s) RETURNING id", (payer_id, amount, int(time.time())))
		id_new_transaction = cur.fetchone()[0]
		dbman.commit_changes()

		cur.execute("INSERT INTO payees (transaction_id, payee) VALUES (%s, %s)", (id_new_transaction, payee_id))
		dbman.close_cursor(cur)
	except Exception as error:
		print("An error occured in /giving command: %s" % error)
		return

	send_markdown_message(bot, chat["id"], "Transaction added successfully!")


def spent(bot, user, chat, args):
	payer_id = int(user["id"])

	if len(args) != 2:
		send_markdown_message(bot, chat["id"], helpers[spent])
		return

	try:
		amountstr = args[0].replace(',', '.').replace('€', '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], "Amount of money not valid.")
		return

	description = args[1]
	# TODO continue...


helpers = {
	authorize: "Usage: `/authorize <user>`",
	deauthorize: "Usage: `/deauthorize <user>`",
	given: "Usage: `/given <amount> <user>`",
	spent: "Usage: `/spent <amount> <description>`. Payees are all the members of the group, including the payer."
}

commands_private = {"authorize": authorize, "deauthorize": deauthorize, "given": given}
commands_group = {"spent": spent}


def handle(bot, msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	chat = msg["chat"]
	user = msg["from"]

	if content_type in ["new_chat_member", "new_chat_members"] and chat_type == "group":  # second cond. maybe useless
		group_id = int(chat_id)
		user_id = int(user["id"])

		group_exists_in_db = dbman.check_existence_group(group_id)  # does the group exists in db?

		# vuol dire che nessuno si è presentato!
		# TODO check I am really me (bot has an unique id)
		if not group_exists_in_db and content_type in ["new_chat_member", "new_chat_members"]:
			# so... I am the new chat member (bot)
				send_markdown_message(bot, chat_id,
		                        "Hello everyone!\nI'm cembot, and I'll help you administrating your expenses!\n"
		                        "Each member should introduce yourself.\n"
		                        "Do it with the command /hereiam (you can click on it)")

		""""  # POTENTIALLY USELESS: I add all the users without distinctions with the command /hereiam
			if content_type == "new_chat_members":
				#TODO add all the users to the group apart BOT
				...

		if group_exists_in_db and content_type == "new_chat_member":
			#TODO add the new member
			...
		if group_exists_in_db and content_type == "new_chat_members":
			#TODO add the new members
			...
		"""

	if content_type == "text":
		parsed = telepot.routing.by_chat_command(pass_args=True, separator=' ')(msg)

		# check if there is a mapping between username and id
		dbman.update_username_id_mapping(user)

		if parsed[0] in commands_private:
			if chat["type"] != "private":
				bot.sendMessage(chat["id"], "For using this command open a private chat with @coexmabot.")
			else:
				commands_private[parsed[0]](bot, user, chat, parsed[1][0])

		if parsed[0] == "hereiam":
			group_id = chat_id
			user_id = user["id"]

			dbman.check_belonging_existence(user_id, group_id) # check and insert if necessary the belonging

			number_members_db = dbman.get_number_members_group(group_id)
			number_members = int(bot.getChatMembersCount(chat["id"])) - 1
			if number_members == number_members_db:
				send_markdown_message(bot, chat["id"], "Ok perfect! Each member has introduced himself!\n"
			                                       "Now we can start things!")
			elif number_members == number_members_db + 1:
				send_markdown_message(bot, chat["id"], "1 person is missing.")
			else:
				send_markdown_message(bot, chat["id"], "%s people are missing.")


		if parsed[0] in commands_group:
			print(msg)
			chat = msg["chat"]
			user = msg["from"]
			if chat["type"] != "group":
				bot.sendMessage(chat["id"], "For using this command add @coexmabot in a group.")
			else:
				commands_group[parsed[0]](bot, user, chat, parsed[1][0])


def main(argv):
	global dbman
	if len(argv) == 4+1:
		dbname = argv[1]
		dbuser = argv[2]
		dbpassword = argv[3]
		dbhost = argv[4]
		dbman = DBManager.DBManager(dbname, dbuser, dbpassword, dbhost)
	else:
		print("Usage: python " + argv[0] + " <dbname> <dbuser> <dbpassword> <dbhost>")
		exit(1)

	bot = telepot.Bot(os.environ["CEM"])
	telepot.loop.MessageLoop(bot, handle=(lambda msg: handle(bot, msg))).run_as_thread()
	print('Listening ...')

	while input() != "q":
		time.sleep(1)

	dbman.close_connection()


if __name__ == "__main__":
	main(sys.argv)
