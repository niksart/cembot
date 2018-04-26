#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot
import telepot.routing
import telepot.loop
import time
import sys
import os
import DBManager


def authorize(bot, user, chat, args):
	authorizer = user["username"]
	authorized = args[0]

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer, authorized))
	if cur.fetchone() is not None:
		bot.sendMessage(chat["id"], "You have already authorized this user.")
	else:
		cur.execute("INSERT INTO authorizations (authorizer, authorized) VALUES (%s, %s)", (authorizer, authorized))
		bot.sendMessage(chat["id"], "User @" + authorized + " has been authorized.")
	dbman.close_cursor(cur)


def deauthorize(bot, user, chat, args):
	deauthorizer = user["username"]
	deauthorized = args[0]

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer, deauthorized))
	if cur.fetchone() is None:
		bot.sendMessage(chat["id"], "You have not already authorized this user. You can't deauthorize it.")
	else:
		cur.execute("DELETE FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer, deauthorized))
		bot.sendMessage(chat["id"], "User @" + deauthorized + " has been deauthorized.")
	dbman.close_cursor(cur)


commands_private = {"authorize": authorize, "deauthorize": deauthorize}
commands_group = {}


def handle(bot, msg):
	parsed = telepot.routing.by_chat_command(pass_args=True, separator=' ')(msg)

	if parsed[0] in commands_private:
		print(msg)
		chat = msg["chat"]
		user = msg["from"]
		if chat["type"] != "private":
			bot.sendMessage(chat["id"], "For using this command open a private chat with @coexmabot.")
		else:
			commands_private[parsed[0]](bot, user, chat, parsed[1][0])


def main(argv):
	global dbman
	if len(argv) == 4+1:
		dbname = argv[1]
		dbuser = argv[2]
		dbpassword = argv[3]
		dbhost = argv[4]
	else:
		print("Usage: python " + argv[0] + " <dbname> <dbuser> <dbpassword> <dbhost>")
		exit(1)
	dbman = DBManager.DBManager(dbname, dbuser, dbpassword, dbhost)
	
	bot = telepot.Bot(os.environ["CEM"])
	telepot.loop.MessageLoop(bot, handle=(lambda msg: handle(bot, msg))).run_as_thread()
	print('Listening ...')

	while input() != "q":
		time.sleep(1)

	dbman.close_connection()


if __name__ == "__main__":
	main(sys.argv)
