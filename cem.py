#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot
import telepot.routing
import telepot.loop
import time
import sys
import os
import DBManager
import info_messages
import error_messages
import commands
import helpers

DEBUG = True


# AUXILIARY FUNCTIONS #


def is_username(s):
	return len(s) - 1 > 4 and s[0] == "@"


def get_function_by_key(key):
	if key == "AUTHORIZE":
		return authorize
	if key == "DEAUTHORIZE":
		return deauthorize
	if key == "GIVEN":
		return given
	if key == "SPENT":
		return spent
	if key == "MYID":
		return myid
	if key == "BALANCE":
		return balance


def set_language(lang):
	global error
	global info
	global commands_group
	global commands_private
	global helper

	lang = lang[:2]

	if lang == "it":  # support for italian
		error = error_messages.IT
		info = info_messages.IT
		commands_group = commands.IT_G
		commands_private = commands.IT_P
		helper = helpers.IT
	else:  # default language: english
		error = error_messages.EN
		info = info_messages.EN
		commands_group = commands.EN_G
		commands_private = commands.EN_P
		helper = helpers.EN


def stringify(list):
	ret = ""
	firstWord = True
	for word in list:
		if firstWord:
			ret = word
			firstWord = False
		else:
			ret = ret + ' ' + word
	return ret


#########################


def authorize(bot, user, chat, args):
	authorizer_id = int(user["id"])

	if len(args) != 1:
		bot.sendMessage(chat["id"], helper["AUTHORIZE"], parse_mode="HTML")
		return

	if is_username(args[0]):
		authorized_username = args[0][1:]
		authorized_id = dbman.get_id_by_username(authorized_username)
	elif (args[0]).isnumeric():
		authorized_id = int(args[0])
		authorized_username = str(authorized_id)
	else:
		bot.sendMessage(chat["id"], error["maybe_you_wrote_an_username_instead_id"])
		return

	# only if user wrote an unregistered username
	if authorized_id is None:
		bot.sendMessage(chat["id"], error["user_unregistered(user)"] % authorized_username, parse_mode="HTML")
		return

	# print("%s: 'please authorize this user: %s'" % (authorizer_id, authorized_id))

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer_id, authorized_id))
	if cur.fetchone() is not None:
		bot.sendMessage(chat["id"], error["have_authorized_yet_this_user"])
	else:
		cur.execute("INSERT INTO authorizations (authorizer, authorized) VALUES (%s, %s)", (authorizer_id, authorized_id))
		bot.sendMessage(chat["id"], info["authorized_confirm(user)"] % authorized_username)
	dbman.close_cursor(cur)


def deauthorize(bot, user, chat, args):
	deauthorizer_id = int(user["id"])

	if len(args) != 1:
		bot.sendMessage(chat["id"], helper["DEAUTHORIZE"], parse_mode="HTML")
		return

	if is_username(args[0]):
		deauthorized_username = args[0][1:]
		deauthorized_id = dbman.get_id_by_username(deauthorized_username)
	elif (args[0]).isnumeric():
		deauthorized_id = int(args[0])
		deauthorized_username = str(deauthorized_id)
	else:
		bot.sendMessage(chat["id"], error["maybe_you_wrote_an_username_instead_id"])
		return


	if deauthorized_id is None:
		bot.sendMessage(chat["id"], error["user_unregistered(user)"] % deauthorized_username, parse_mode="HTML")
		return

	# print("%s: 'please deauthorize this user: %s'" % (deauthorizer_id, deauthorized_id))

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer_id, deauthorized_id))
	if cur.fetchone() is None:
		bot.sendMessage(chat["id"], error["can't_deauthorize_cause_not_authorized_yet"])
	else:
		cur.execute("DELETE FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer_id, deauthorized_id))
		bot.sendMessage(chat["id"], info["deauthorized_confirm(user)"] % deauthorized_username)
	dbman.close_cursor(cur)


def given(bot, user, chat, args):
	payer_id = int(user["id"])

	if len(args) < 3:
		bot.sendMessage(chat["id"], helper["GIVEN"], parse_mode="HTML")
		return

	try:
		amountstr = args[0].replace(',', '.').replace('€', '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], error["amount_money_not_valid"])
		return

	if is_username(args[1]):
		payee_username = args[1][1:]
		payee_id = dbman.get_id_by_username(payee_username)
	elif (args[1]).isnumeric():
		payee_id = int(args[1])
		payee_username = str(payee_id)
	else:
		bot.sendMessage(chat["id"], error["maybe_you_wrote_an_username_instead_id"])
		return

	description = stringify(args[2:])

	if payee_id is None:
		bot.sendMessage(chat["id"], error["user_unregistered(user)"] % payee_username, parse_mode="HTML")
		return

	if not dbman.test_authorization(payee_id, payer_id):  # if payee has not authorized the payer exit
		bot.sendMessage(chat["id"], error["lack_of_authorization(user)"] % payee_username, parse_mode="HTML")
		return

	try:
		cur = dbman.get_cursor()
		cur.execute("INSERT INTO transactions (payer, amount, time, description) VALUES (%s, %s, %s, %s) RETURNING id", (payer_id, amount, int(time.time()), description))
		id_new_transaction = cur.fetchone()[0]
		dbman.commit_changes()

		cur.execute("INSERT INTO payees (transaction_id, payee) VALUES (%s, %s)", (id_new_transaction, payee_id))
		dbman.close_cursor(cur)
	except Exception as e:
		print("An error occured in /giving command: %s" % e)
		dbman.conn.rollback()
		return

	bot.sendMessage(chat["id"], info["transaction_succeed"], parse_mode="HTML")


def spent(bot, user, chat, args):
	payer_id = int(user["id"])

	if len(args) < 2:
		bot.sendMessage(chat["id"], helper["SPENT"], parse_mode="HTML")
		return

	try:
		amountstr = args[0].replace(',', '.').replace('€', '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], error["amount_money_not_valid"])
		return

	description = stringify(args[1:])

	try:
		cur = dbman.get_cursor()
		cur.execute("INSERT INTO transactions (payer, description, amount, time, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", (payer_id, description, amount, int(time.time()), chat["id"]))
		id_new_transaction = cur.fetchone()[0]
		dbman.commit_changes()

		# get all id of the group
		users = dbman.get_id_members_by_group(chat["id"])

		# inserisci n payees, uno per ogni appartenente al gruppo
		for payee_id in users:
			cur.execute("INSERT INTO payees (transaction_id, payee) VALUES (%s, %s)", (id_new_transaction, payee_id))

		dbman.close_cursor(cur)
	except Exception as e:
		print("An error occured in /spent command: %s" % e)
		dbman.conn.rollback()
		return

	bot.sendMessage(chat["id"], info["transaction_succeed"], parse_mode="HTML")


def myid(bot, user, chat, args):
	if len(args) != 0:
		bot.sendMessage(chat["id"], helper["MYID"], parse_mode="HTML")
		return
	bot.sendMessage(chat["id"], info["your_id_is(id)"] % user["id"])


def balance(bot, user, chat, args):
	user1_id = user["id"]

	if len(args) == 0:
		# bilancio totale
		people = dbman.get_set_users_involved_with_me(user1_id)
		message = ""
		for user2_id in people:
			user2_username = dbman.get_username_by_id(user2_id)
			if user2_username == None:
				user2 = user2_id
			else:
				user2 = "@" + user2_username
			message += info["balance_with_other_user(user,balance)"] % (user2, dbman.get_balance(user1_id, user2_id)) + "\n"
		bot.sendMessage(chat["id"], message, parse_mode="HTML")
	elif len(args) == 1:
		# bilancio verso user
		if is_username(args[0]):
			user2_username = args[0][1:]
			user2_id = dbman.get_id_by_username(user2_username)
		elif (args[0]).isnumeric():
			user2_id = int(args[0])
			user2_username = None
		else:
			bot.sendMessage(chat["id"], error["maybe_you_wrote_an_username_instead_id"])
			return
		# ora ho user1_id e user2_id
		if user2_username == None:
			user2 = user2_id
		else:
			user2 = "@" + user2_username
		bot.sendMessage(chat["id"], info["balance_with_other_user(user,balance)"] % (user2, dbman.get_balance(user1_id, user2_id)))
	else:
		bot.sendMessage(chat["id"], helper["BALANCE"], parse_mode="HTML")
		return


def handle(bot, msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	if DEBUG:
		print(msg)

	chat = msg["chat"]
	user = msg["from"]
	set_language(user["language_code"])

	# check if there is a mapping between username and id in db
	dbman.update_username_id_mapping(user)

	# c'è un nuovo membro nel gruppo
	if content_type == "new_chat_member" and chat_type == "group":
		added_user = msg["new_chat_member"]["id"]
		if added_user == bot_id:
			bot.sendMessage(chat_id, info["introduced_in_group"])
		else:
			dbman.check_belonging_existence(added_user, chat_id)

	if content_type == "left_chat_member" and chat_type == "group":
		removed_user = msg["left_chat_member"]["id"]
		dbman.remove_belonging(removed_user, chat_id)

	# o se sono stato aggiunto al momento della creazione del gruppo invio il messaggio
	if content_type == "group_chat_created":
		bot.sendMessage(chat_id, info["introduced_in_group"])

	if content_type == "text":
		parsed = telepot.routing.by_chat_command(pass_args=True, separator=' ')(msg)
		command_typed = parsed[0]
		text_after_command = parsed[1][0]

		if command_typed in commands_private:
			if chat["type"] == "private":
				get_function_by_key(commands_private[command_typed])(bot, user, chat, text_after_command)
			else:
				bot.sendMessage(chat["id"], error["command_unavailable_for_private"])

		if command_typed in commands_group:
			if chat["type"] == "group":
				if commands_group[command_typed] == "PRESENTATION":  # l'utente si è presentato
					group_id = chat_id
					user_id = user["id"]

					dbman.check_belonging_existence(user_id, group_id)  # check and insert if necessary the belonging

					number_members_db = dbman.get_number_members_group(group_id)
					number_members = int(bot.getChatMembersCount(chat["id"])) - 1
					if number_members == number_members_db:
						bot.sendMessage(chat["id"], info["each_member_introduced"], parse_mode="HTML")
					elif number_members == number_members_db + 1:
						bot.sendMessage(chat["id"], info["person_missing"], parse_mode="HTML")
					else:
						bot.sendMessage(chat["id"], "%s" + info["people_missing"], parse_mode="HTML")
				else:
					get_function_by_key(commands_group[command_typed])(bot, user, chat, text_after_command)
			else:
				bot.sendMessage(chat["id"], error["command_unavailable_for_group"])


def main(argv):
	global dbman
	global bot_id
	if len(argv) == 4 + 1:
		dbname = argv[1]
		dbuser = argv[2]
		dbpassword = argv[3]
		dbhost = argv[4]
		dbman = DBManager.DBManager(dbname, dbuser, dbpassword, dbhost)
	else:
		print("Usage: python " + argv[0] + " <dbname> <dbuser> <dbpassword> <dbhost>")
		exit(1)

	bot = telepot.Bot(os.environ["CEM"])
	bot_id = bot.getMe()["id"]

	telepot.loop.MessageLoop(bot, handle=(lambda msg: handle(bot, msg))).run_as_thread()
	print('Listening ...')

	while input() != "q":
		time.sleep(1)

	dbman.close_connection()


if __name__ == "__main__":
	main(sys.argv)
