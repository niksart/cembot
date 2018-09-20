def last_loans(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	if len(args) > 1:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["LAST_LOANS"], parse_mode=parse_mode)
		return

	n_max_loans = 0

	if len(args) == 0:
		n_max_loans = 5
	elif len(args) == 1:
		try:
			n_max_charges = int(args[0])
		except ValueError:
			bot.sendMessage(chat["id"], LANG["error"]["insert_a_correct_number"])
			return

	if n_max_loans < 0 or n_max_loans > 100:
		n_max_loans = 5

	(individual_loans, group_loans) = dbman.get_last_n_loans(chat["id"], n_max_loans)
	message = ""

	if individual_loans != ():
		message = LANG["info"]["these_are_the_last_individual_loans"]
		for (payer, amount, description) in individual_loans:
			message += "▪️ " + (payer if payer.isnumeric() else "@" + payer) + ", " + "{:=.2f}".format(
				amount) + " " + currency + ", " + str(description) + "\n"

	if group_loans != ():
		message += "\n🔷 🔷 🔷\n\n"
		message += LANG["info"]["these_are_the_last_group_loans"]
		for (group_name, amount, description) in group_loans:
			message += "▫️ " + group_name + ", " + "{:=.2f}".format(amount) + " " + currency + ", " + str(description) + "\n"

	if individual_loans == () and group_loans == ():
		message += LANG["info"]["no_loans_yet"]

	bot.sendMessage(chat["id"], message)
