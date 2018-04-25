#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot
import telepot.routing
import sqlite3
import os

dbfile = "../cem.db"


def authorize(bot, user, chat, args):
	authorizer = user["username"]
	authorizee = args[0]

	conn = sqlite3.connect(dbfile)
	db = conn.cursor()
	db.execute("SELECT id FROM authorizations WHERE authorizer=:azer AND authorizee=:azee",
	           {"azer": authorizer, "azee": authorizee})
	if db.fetchone() is not None:
		bot.sendMessage(chat["id"], "You have already authorized this user.")
	else:
		db.execute("INSERT INTO authorizations (authorizer, authorizee) VALUES (?, ?)", (authorizer, authorizee))
		bot.sendMessage(chat["id"], "User @" + authorizee + " has been authorized.")
	conn.commit()
	db.close()


def deauthorize(bot, user, chat, args):
	deauthorizer = user["username"]
	deauthorizee = args[0]

	conn = sqlite3.connect(dbfile)
	db = conn.cursor()
	db.execute("SELECT id FROM authorizations WHERE authorizer=:authorizer AND authorizee=:authorizee",
	           {"authorizer": deauthorizer, "authorizee": deauthorizee})
	if db.fetchone() is None:
		bot.sendMessage(chat["id"], "You have not already authorized this user. You can't deauthorize it.")
	else:
		db.execute("DELETE FROM authorizations WHERE authorizer=:deauthorizer AND authorizee=:deauthorizee",
		           {"deauthorizer": deauthorizer, "deauthorizee": deauthorizee})
		bot.sendMessage(chat["id"], "User @" + deauthorizee + " has been deauthorized.")
	conn.commit()
	db.close()


commands_private = {"authorize": authorize, "deauthorize": deauthorize}
commands_group = {}


def handle(bot, msg):
	parsed = telepot.routing.by_chat_command(pass_args=True, separator=' ')(msg)

	if parsed[0] in commands_private:
		chat = msg["chat"]
		user = msg["from"]
		if chat["type"] != "private":
			bot.sendMessage(chat["id"], "For using this command open a private chat with @coexmabot.")
		else:
			commands_private[parsed[0]](bot, user, chat, parsed[1][0])


def main():
	bot = telepot.Bot(os.environ["CEM"])
	bot.message_loop(lambda x: handle(bot, x), run_forever=True)


if __name__ == "__main__":
	main()
