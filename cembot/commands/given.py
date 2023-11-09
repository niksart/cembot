from utils import auxiliary_functions
import time
import logging

def given(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	payer_id = int(user["id"])

	if len(args) < 3:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["GIVEN"], parse_mode=parse_mode)
		return

	try:
		amountstr = args[0].replace(',', '.').replace(currency, '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], LANG["error"]["amount_money_not_valid"])
		return

	if auxiliary_functions.is_username(args[1]):
		payee_username = args[1][1:]
		payee_id = dbman.get_id_by_username(payee_username)
	elif (args[1]).isnumeric():
		payee_id = int(args[1])
		payee_username = str(payee_id)
	else:
		bot.sendMessage(chat["id"], LANG["error"]["maybe_you_wrote_an_username_instead_id"])
		return

	description = auxiliary_functions.stringify(args[2:])

	if payee_id is None:
		bot.sendMessage(chat["id"], LANG["error"]["user_unregistered(user)"] % payee_username, parse_mode=parse_mode)
		return

	if not dbman.test_authorization(payee_id, payer_id):  # if payee has not authorized the payer exit
		bot.sendMessage(chat["id"], LANG["error"]["lack_of_authorization(user)"] % payee_username, parse_mode=parse_mode)
		return

	try:
		cur = dbman.get_cursor()
		cur.execute("INSERT INTO transactions (payer, amount, time, description) VALUES (%s, %s, %s, %s) RETURNING id", (payer_id, amount, int(time.time()), description))
		id_new_transaction = cur.fetchone()[0]
		dbman.commit_changes()

		cur.execute("INSERT INTO payees (transaction_id, payee) VALUES (%s, %s)", (id_new_transaction, payee_id))
		dbman.close_cursor(cur)
	except Exception as e:
		logging.error("An error occured in /giving command: %s" % e)
		dbman.conn.rollback()
		return

	bot.sendMessage(chat["id"], LANG["info"]["transaction_succeed"], parse_mode=parse_mode)

