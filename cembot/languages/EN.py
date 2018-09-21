# Support for english (EN) language

helper_commands = {
	"AUTHORIZE": "Usage:\n/authorize @<username>\n/authorize <user id>",
	"DEAUTHORIZE": "Usage:\n/deauthorize @<username>\n/deauthorize <user id>",
	"GIVEN": "Usage:\n/given <amount> @<username> <description>",
	"SPENT": "Usage:\n/spent <amount> <description>.\nPayees are all the members of the group, including the payer.",
	"MYID": ...,
	"START": ...,
	"LAST_GROUP_EXPENSES": ...,
	"LAST_CHARGES": ...,
	"LAST_LOANS": ...
}

info = {
	"start": ...,
	"guide": ...,
	"introduced_in_group": "Hello everyone!\nI'm cembot, and I'll help you administrating your expenses!\n"
	                       "Each member of this group now should introduce yourself. "
	                       "People added after this message can avoid to introduce themselves.\n"
	                       "Do it with the command /hereIam",
	"each_member_introduced": ...,
	"person_missing": "1 person is missing.",
	"people_missing": " people are missing.",
	"transaction_succeed": "Transaction added successfully!",
	"authorized_confirm(user)": "User @%s has been authorized.",
	"deauthorized_confirm(user)": "The authorization of user @%s has been revoked.",
	"your_id_is(id)": "Your Telegram id is %s. You can add in Telegram settings an username and use cembot more easily.",
	"balance_with_other_user(user,balance)": "Your balance with the user %s is %s",
	"header_balance_credit": "📗 Credits\n",
	"header_balance_debit": "📕 Debits\n",
	"commands": ...,
	"these_are_the_last_group_expenses": ...,
	"these_are_the_last_individual_charges": ...,
	"these_are_the_last_group_charges": ...,
	"no_charges_yet": ...,
	"these_are_the_last_individual_loans": ...,
	"these_are_the_last_group_loans": ...
}

error = {
	"command_unavailable_for_private": "For using this command open a private chat with @en_cembot.",
	"command_unavailable_for_group": "For using this command add @en_cembot in a group.",
	"amount_money_not_valid": "Amount of money not valid.",
	"waiting_for_all_users": ...,
	"lack_of_authorization(user)": "The user @%s has not authorized you for charging expenses.",
	"user_unregistered(user)": "The user @%s that you want to add as a payee is not registered on our system",
	"can't_deauthorize_cause_not_authorized_yet": "You have not already authorized this user. You can't deauthorize it.",
	"have_authorized_yet_this_user": "You have already authorized this user.",
	"maybe_you_wrote_an_username_instead_id": "This is not a numeric id. If you intended to write an username write it with a @ at the beginning.",
	"insert_a_correct_number": ...
}

# commands

private_commands = {
	"start": "START",
	"commands": "COMMANDS",
	"authorize": "AUTHORIZE",
	"revoke": "DEAUTHORIZE",
	"given": "GIVEN",
	"myid": "MYID",
	"balance": "BALANCE",
	"last_charges": "LAST_CHARGES",
	"last_loans": "LAST_LOANS",
	"guide": "GUIDE"
}

group_commands = {
	"spent": "SPENT",
	"spent@en_cembot": "SPENT", # version with @[language]_cembot

	"hereIam": "PRESENTATION",
	"hereIam@en_cembot": "PRESENTATION", # version with @[language]_cembot

	"last_expenses": "LAST_GROUP_EXPENSES",
	"last_expenses@en_cembot": "LAST_GROUP_EXPENSES", # version with @[language]_cembot
}
