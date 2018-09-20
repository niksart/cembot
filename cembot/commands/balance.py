from utils import auxiliary_functions

def balance(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	user1_id = user["id"]

	if len(args) == 0:
		# bilancio totale
		people = dbman.get_set_users_involved_with_me(user1_id)
		message_credit = ""
		message_debit = ""

		for user2_id in people:
			user2_username = dbman.get_username_by_id(user2_id)
			if user2_username is None:
				user2 = user2_id
			else:
				user2 = "@" + user2_username
			credit_or_debit = dbman.get_balance(user1_id, user2_id)
			credit_or_debit_string = "{:=+7.2f}".format(credit_or_debit)

			if credit_or_debit > 0:
				message_credit += "%s, %s " % (user2, credit_or_debit_string) + currency + "\n"
			elif credit_or_debit < 0:
				message_debit += "%s, %s " % (user2, credit_or_debit_string) + currency + "\n"

		message = LANG["info"]["header_balance_credit"]
		message += message_credit
		message += "\n"
		message += LANG["info"]["header_balance_debit"]
		message += message_debit
		bot.sendMessage(chat["id"], message, parse_mode=parse_mode)
	elif len(args) == 1:
		# bilancio verso user
		if auxiliary_functions.is_username(args[0]):
			user2_username = args[0][1:]
			user2_id = dbman.get_id_by_username(user2_username)
		elif (args[0]).isnumeric():
			user2_id = int(args[0])
			user2_username = None
		else:
			bot.sendMessage(chat["id"], LANG["error"]["maybe_you_wrote_an_username_instead_id"])
			return
		# ora ho user1_id e user2_id
		if user2_username is None:
			user2 = user2_id
		else:
			user2 = "@" + user2_username
		bot.sendMessage(chat["id"], LANG["info"]["balance_with_other_user(user,balance)"] % (user2, "{:=+7.2f}".format(dbman.get_balance(user1_id, user2_id))))
	else:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["BALANCE"], parse_mode=parse_mode)
		return
