def guide(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	bot.sendMessage(chat["id"], LANG["info"]["guide"])
