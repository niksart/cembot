def myid(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	if len(args) != 0:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["MYID"], parse_mode=parse_mode)
		return
	bot.sendMessage(chat["id"], LANG["info"]["your_id_is(id)"] % user["id"])
