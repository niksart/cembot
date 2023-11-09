#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telepot
import telepot.routing
import telepot.loop
import telepot.text

import sys
import os
import logging

import DBManager
import languages
import commands

bot_token_env_variable = "CEM_TELEGRAM_TOKEN"


def set_language(lang):
	global LANG

	lang = lang[:2]

	if lang == "IT":  # support for italian IT
		LANG = {
			"error": languages.IT.error,
			"info": languages.IT.info,
			"group_commands": languages.IT.group_commands,
			"private_commands": languages.IT.private_commands,
			"helper_commands": languages.IT.helper_commands
		}
	else:  # default language: english EN
		LANG = {
			"error": languages.EN.error,
			"info": languages.EN.info,
			"group_commands": languages.EN.group_commands,
			"private_commands": languages.EN.private_commands,
			"helper_commands": languages.EN.helper_commands
		}


def handle(bot, msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	logging.debug(msg)

	chat = msg["chat"]
	user = msg["from"]

	# check if there is a mapping between username and id in db
	dbman.update_username_id_mapping(user)

	# c'è un nuovo membro nel gruppo
	if content_type == "new_chat_member" and chat_type in ["group", "supergroup"]:
		added_user = msg["new_chat_member"]["id"]
		if added_user == bot_id:
			bot.sendMessage(chat_id, LANG["info"]["introduced_in_group"])
		else:
			dbman.check_belonging_existence(added_user, chat_id)

	if content_type == "left_chat_member" and chat_type in ["group", "supergroup"]:
		removed_user = msg["left_chat_member"]["id"]
		dbman.remove_belonging(removed_user, chat_id)

	# o se sono stato aggiunto al momento della creazione del gruppo invio il messaggio
	if content_type == "group_chat_created":
		bot.sendMessage(chat_id, LANG["info"]["introduced_in_group"])

	if content_type == "text":
		parsed = telepot.routing.by_chat_command(pass_args=True, separator=' ')(msg)
		command_typed = parsed[0]
		text_after_command = parsed[1][0]

		if command_typed in LANG["private_commands"]:
			if chat["type"] == "private":
				commands_by_key[LANG["private_commands"][command_typed]](bot, user, chat, text_after_command, dbman, LANG, currency, parse_mode)
			else:
				bot.sendMessage(chat["id"], LANG["error"]["command_unavailable_for_private"])

		if command_typed in LANG["group_commands"]:
			if chat["type"] in ["group", "supergroup"]:
				group_id = chat_id
				group_name = chat["title"]
				dbman.update_groupname_id_mappings(group_id, group_name)
				if LANG["group_commands"][command_typed] == "PRESENTATION":  # l'utente si è presentato
					user_id = user["id"]
					dbman.check_belonging_existence(user_id, group_id)  # check and insert if necessary the belonging

					number_members_db = dbman.get_number_members_group(group_id)
					number_members = int(bot.getChatMembersCount(chat["id"])) - 1
					if number_members == number_members_db:
						bot.sendMessage(chat["id"], LANG["info"]["each_member_introduced"], parse_mode=parse_mode)
					elif number_members == number_members_db + 1:
						bot.sendMessage(chat["id"], LANG["info"]["person_missing"], parse_mode=parse_mode)
					else:
						bot.sendMessage(chat["id"], "%s" + LANG["info"]["people_missing"], parse_mode=parse_mode)
				else:
					commands_by_key[LANG["group_commands"][command_typed]](bot, user, chat, text_after_command, dbman, LANG, currency, parse_mode)
			else:
				bot.sendMessage(chat["id"], LANG["error"]["command_unavailable_for_group"], parse_mode=parse_mode)


def main(argv):
	global dbman
	global bot_id
	global parse_mode

	global currency

	parse_mode = None
	
	if len(argv) == 5 + 1:
		dbname = argv[1]
		dbuser = argv[2]
		dbpassword = argv[3]
		dbhost = argv[4]
		botlanguage = argv[5].upper()
		currency = argv[6]

		set_language(botlanguage)

		dbman = DBManager.DBManager.DBManager(dbname, dbuser, dbpassword, dbhost)

		bot = telepot.Bot(os.environ[bot_token_env_variable])
		bot_id = bot.getMe()["id"]

		try:
			telepot.loop.MessageLoop(bot, handle=(lambda msg: handle(bot, msg))).run_forever()
		except:
			dbman.close_connection()
	else:
		print("Usage: python " + argv[0] + " <dbname> <dbuser> <dbpassword> <dbhost> <IT | EN for language> <currency>")
		exit(1)


commands_by_key = {
	"AUTHORIZE": commands.authorize.authorize,
	"DEAUTHORIZE": commands.deauthorize.deauthorize,
	"GIVEN": commands.given.given,
	"SPENT": commands.spent.spent,
	"MYID": commands.myid.myid,
	"BALANCE": commands.balance.balance,
	"START": commands.start.start,
	"COMMANDS": commands.commands_list.commands_list,
	"LAST_GROUP_EXPENSES": commands.last_group_expenses.last_group_expenses,
	"LAST_LOANS": commands.last_loans.last_loans,
	"LAST_CHARGES": commands.last_charges.last_charges,
	"GUIDE": commands.guide.guide
}

if __name__ == "__main__":
	main(sys.argv)
