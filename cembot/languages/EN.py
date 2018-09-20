EN_P = {"start": "START", "commands": "COMMANDS", "authorize": "AUTHORIZE", "deauthorize": "DEAUTHORIZE", "given": "GIVEN", "myid": "MYID", "balance": "BALANCE"} #private
EN_G = {"spent": "SPENT", "hereiam": "PRESENTATION"} #group


EN = {
	"command_unavailable_for_private": "For using this command open a private chat with @en_cembot.",
	"command_unavailable_for_group": "For using this command add @coexmabot in a group.",
	"amount_money_not_valid": "Amount of money not valid.",

    "lack_of_authorization(user)": "The user @%s has not authorized you for charging expenses.",
	"user_unregistered(user)": "The user @%s that you want to add as a payee is not registered on our system",
	"can't_deauthorize_cause_not_authorized_yet": "You have not already authorized this user. You can't deauthorize it.",
	"have_authorized_yet_this_user": "You have already authorized this user.",
	"maybe_you_wrote_an_username_instead_id": "This is not a numeric id. If you intended to write an username write it with a @ at the beginning."
}


EN = {
	"AUTHORIZE": "Usage:\n/authorize @<username>\n/authorize <user id>",
	"DEAUTHORIZE": "Usage:\n/deauthorize @<username>\n/deauthorize <user id>",
	"GIVEN": "Usage:\n/given <amount> @<username> <description>",
	"SPENT": "Usage:\n/spent <amount> <description>.\nPayees are all the members of the group, including the payer.",
	"MYID": ""
}


EN = {
	"start": "",
	"introduced_in_group": "Hello everyone!\nI'm cembot, and I'll help you administrating your expenses!\n"
	                       "Each member of this group now should introduce yourself. "
	                       "People added after this message can avoid to introduce themselves.\n"
	                       "Do it with the command /hereiam",
	"each_member_introduced": "Ok perfect! Each member has introduced himself!\nNow we can start!",
	"person_missing": "1 person is missing.",
	"people_missing": " people are missing.",

	"transaction_succeed": "Transaction added successfully!",

	"authorized_confirm(user)": "User @%s has been authorized.",
	"deauthorized_confirm(user)": "User @%s has been deauthorized.",
	"your_id_is(id)": "Your Telegram id is %s. You can add in Telegram settings an username and use cembot more easily.",
	"balance_with_other_user(user,balance)": "Your balance with the user %s is %s",
	"header_balance_credit": "📗 Credits\n",
	"header_balance_debit": "📕 Debits\n"
}