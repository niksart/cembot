def last_charges(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	if len(args) > 1:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["LAST_CHARGES"], parse_mode=parse_mode)
		return

	n_max_charges = 0

	if len(args) == 0:
		n_max_charges = 5
	elif len(args) == 1:
		try:
			n_max_charges = int(args[0])
		except ValueError:
			bot.sendMessage(chat["id"], LANG["error"]["insert_a_correct_number"])
			return

	if n_max_charges < 0 or n_max_charges > 100:
		n_max_charges = 5

	(individual_charges, group_charges) = dbman.get_last_n_charges(chat["id"], n_max_charges)
	message = ""

	if individual_charges != ():
		message = LANG["info"]["these_are_the_last_individual_charges"]
		for (payer, amount, description) in individual_charges:
			message += "▪️ " + (payer if payer.isnumeric() else "@" + payer) + ", " + "{:=.2f}".format(amount) + " " + currency + ", " + str(description) + "\n"

	if group_charges != ():
		message += "\n🔶 🔶 🔶\n\n"
		message += LANG["info"]["these_are_the_last_group_charges"]
		for (payer, amount, description, group_name) in group_charges:
			message += "▫️ " + (payer if payer.isnumeric() else "@" + payer) + ", " + group_name + ", " + "{:=.2f}".format(amount) + " " + currency + ", " + str(description) + "\n"

	if individual_charges == () and group_charges == ():
		message += LANG["info"]["no_charges_yet"]

	bot.sendMessage(chat["id"], message)
