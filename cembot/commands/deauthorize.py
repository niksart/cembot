from utils import auxiliary_functions

def deauthorize(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	deauthorizer_id = int(user["id"])

	if len(args) != 1:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["DEAUTHORIZE"], parse_mode=parse_mode)
		return

	if auxiliary_functions.is_username(args[0]):
		deauthorized_username = args[0][1:]
		deauthorized_id = dbman.get_id_by_username(deauthorized_username)
	elif (args[0]).isnumeric():
		deauthorized_id = int(args[0])
		deauthorized_username = str(deauthorized_id)
	else:
		bot.sendMessage(chat["id"], LANG["error"]["maybe_you_wrote_an_username_instead_id"])
		return

	if deauthorized_id is None:
		bot.sendMessage(chat["id"], LANG["error"]["user_unregistered(user)"] % deauthorized_username, parse_mode=parse_mode)
		return

	# logging.debug("%s: 'please deauthorize this user: %s'" % (deauthorizer_id, deauthorized_id))

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer_id, deauthorized_id))
	if cur.fetchone() is None:
		bot.sendMessage(chat["id"], LANG["error"]["can't_deauthorize_cause_not_authorized_yet"])
	else:
		cur.execute("DELETE FROM authorizations WHERE authorizer=%s AND authorized=%s", (deauthorizer_id, deauthorized_id))
		bot.sendMessage(chat["id"], LANG["info"]["deauthorized_confirm(user)"] % deauthorized_username)
	dbman.close_cursor(cur)
