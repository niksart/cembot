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
	authorizer = user["id"]

	if len(args) != 1:
		send_markdown_message(bot, chat["id"], helpers[authorize])
		return

	authorized = args[0]
	print(authorizer + ": 'please authorize this user: " + authorized + "'")

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer, authorized))
	if cur.fetchone() is not None:
		bot.sendMessage(chat["id"], "You have already authorized this user.")
	else:
		cur.execute("INSERT INTO authorizations (authorizer, authorized) VALUES (%s, %s)", (authorizer, authorized))
		bot.sendMessage(chat["id"], "User @" + authorized + " has been authorized.")
	dbman.close_cursor(cur)


def deauthorize(bot, user, chat, args):
	deauthorizer = user["id"]

	if len(args) != 1:
		send_markdown_message(bot, chat["id"], helpers[deauthorize])
		return

	deauthorized = args[0]
	print(deauthorizer + ": 'please deauthorize this user: " + deauthorized + "'")

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer, deauthorized))
	if cur.fetchone() is None:
		bot.sendMessage(chat["id"], "You have not already authorized this user. You can't deauthorize it.")
	else:
		cur.execute("DELETE FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer, deauthorized))
		bot.sendMessage(chat["id"], "User @" + deauthorized + " has been deauthorized.")
	dbman.close_cursor(cur)


def given(bot, user, chat, args):
	payer = user["id"]

	if len(args) != 2:
		send_markdown_message(bot, chat["id"], helpers[given])
		return

	try:
		amountstr = args[0].replace(',', '.').replace('€', '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], "Amount of money not valid.")
		return

	payee = args[1]

	cur = dbman.get_cursor()
	cur.execute("INSERT INTO transactions (payer, amount, time) VALUES (%s, %s, %s) RETURNING id", (payer, amount, int(time.time())))
	id_new_transaction = cur.fetchone()[0]
	dbman.commit_changes()

	cur.execute("INSERT INTO payees (transaction_id, payee) VALUES (%s, %s)", (id_new_transaction, payee))
	dbman.close_cursor(cur)


helpers = {
	authorize: "Usage: `/authorize <user>`",
	deauthorize: "Usage: `/deauthorize <user>`",
	given: "Usage: `/given <amount> <user>`"
}

commands_private = {"authorize": authorize, "deauthorize": deauthorize, "given": given}
commands_group = {}


def handle(bot, msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	if content_type == 'text':
		parsed = telepot.routing.by_chat_command(pass_args=True, separator=' ')(msg)

		if parsed[0] in commands_private:
			chat = msg["chat"]
			user = msg["from"]
			if chat["type"] != "private":
				bot.sendMessage(chat["id"], "For using this command open a private chat with @coexmabot.")
			else:
				commands_private[parsed[0]](bot, user, chat, parsed[1][0])

		cur = dbman.get_cursor()
		cur.execute("SELECT * FROM idmappings WHERE username=%s", msg["from"]["username"])
		if cur.fetchone() is None:
			cur.execute("INSERT INTO idmappings (username, id) VALUES (%s,%s)", (msg["from"]["username"], msg["from"]["id"]))
		dbman.close_cursor(cur)


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
