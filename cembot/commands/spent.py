from utils import auxiliary_functions
import time
import logging

def spent(bot, user, chat, args, dbman, LANG, currency, parse_mode):
	payer_id = int(user["id"])

	if len(args) < 2:
		bot.sendMessage(chat["id"], LANG["helper_commands"]["SPENT"], parse_mode=parse_mode)
		return

	try:
		amountstr = args[0].replace(',', '.').replace('€', '')
		amount = int(100 * float(amountstr))
	except ValueError:
		bot.sendMessage(chat["id"], LANG["error"]["amount_money_not_valid"])
		return

	description = auxiliary_functions.stringify(args[1:])

	number_members_group_db = dbman.get_number_members_group(chat["id"])
	number_members_group_telegram = int(bot.getChatMembersCount(chat["id"])) - 1

	if number_members_group_db == number_members_group_telegram:
		try:
			cur = dbman.get_cursor()
			cur.execute("INSERT INTO transactions (payer, description, amount, time, group_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", (payer_id, description, amount, int(time.time()), chat["id"]))
			id_new_transaction = cur.fetchone()[0]
			dbman.commit_changes()

			# get all id of the group
			users = dbman.get_id_members_by_group(chat["id"])

			# inserisci n payees, uno per ogni appartenente al gruppo
			for payee_id in users:
				cur.execute("INSERT INTO payees (transaction_id, payee) VALUES (%s, %s)", (id_new_transaction, payee_id))

			dbman.close_cursor(cur)
		except Exception as e:
			logging.error("An error occured in /spent command: %s" % e)
			dbman.conn.rollback()
			return

		bot.sendMessage(chat["id"], LANG["info"]["transaction_succeed"], parse_mode=parse_mode)
	else:
		bot.sendMessage(chat["id"], LANG["error"]["waiting_for_all_users"], parse_mode=parse_mode)
