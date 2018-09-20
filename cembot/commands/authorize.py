from utils import auxiliary_functions

def authorize(bot, user, chat, args, dbman, LANG, currency, parse_mode):

	authorizer_id = int(user["id"])

	if len(args) != 1:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["AUTHORIZE"], parse_mode=parse_mode)
		return

	if auxiliary_functions.is_username(args[0]):
		authorized_username = args[0][1:]
		authorized_id = dbman.get_id_by_username(authorized_username)
	elif (args[0]).isnumeric():
		authorized_id = int(args[0])
		authorized_username = str(authorized_id)
	else:
		bot.sendMessage(chat["id"], LANG["error"]["maybe_you_wrote_an_username_instead_id"])
		return

	# only if user wrote an unregistered username
	if authorized_id is None:
		bot.sendMessage(chat["id"], LANG["error"]["user_unregistered(user)"] % authorized_username, parse_mode=parse_mode)
		return

	cur = dbman.get_cursor()
	cur.execute("SELECT id FROM authorizations WHERE authorizer=%s AND authorized=%s", (authorizer_id, authorized_id))
	if cur.fetchone() is not None:
		bot.sendMessage(chat["id"], LANG["error"]["have_authorized_yet_this_user"])
	else:
		cur.execute("INSERT INTO authorizations (authorizer, authorized) VALUES (%s, %s)", (authorizer_id, authorized_id))
		bot.sendMessage(chat["id"], LANG["info"]["authorized_confirm(user)"] % authorized_username)
	dbman.close_cursor(cur)
