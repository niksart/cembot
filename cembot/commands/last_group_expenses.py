def last_group_expenses(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	if len(args) > 1:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["LAST_GROUP_EXPENSES"], parse_mode=parse_mode)
		return

	n_max_expenses = 0

	if len(args) == 0:
		n_max_expenses = 5
	elif len(args) == 1:
		try:
			n_max_expenses = int(args[0])
		except ValueError:
			bot.sendMessage(chat["id"], LANG["error"]["insert_a_correct_number"])
			return

	if n_max_expenses < 0 or n_max_expenses > 100:
		n_max_expenses = 5
	expenses = dbman.get_last_n_group_expenses(chat["id"], n_max_expenses)
	message = LANG["info"]["these_are_the_last_group_expenses"]
	for (payer, amount, description) in expenses:
		message += "▪️ " + (payer if payer.isnumeric() else "@" + payer) + ", " + "{:=.2f}".format(amount) + " " + currency + ", " + description + "\n"

	bot.sendMessage(chat["id"], message)
