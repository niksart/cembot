# Support for [language] ([code language]) language

helper_commands = {
	"AUTHORIZE": ...,
	"DEAUTHORIZE": ...,
	"GIVEN": ...,
	"SPENT": ...,
	"MYID": ...,
	"START": ...,
	"LAST_GROUP_EXPENSES": ...,
	"LAST_CHARGES": ...,
	"LAST_LOANS": ...
}

info = {
	"start": ...,
	"guide": ...,
	"introduced_in_group": ...,
	"each_member_introduced": ...,
	"person_missing": ...,
	"people_missing": ...,
	"transaction_succeed": ...,
	"authorized_confirm(user)": ...,
	"deauthorized_confirm(user)": ...,
	"your_id_is(id)": ...,
	"balance_with_other_user(user,balance)": ...,
	"header_balance_credit": ...,
	"header_balance_debit": ...,
	"commands": ...,
	"these_are_the_last_group_expenses": ...,
	"these_are_the_last_individual_charges": ...,
	"these_are_the_last_group_charges": ...,
	"no_charges_yet": ...,
	"these_are_the_last_individual_loans": ...,
	"these_are_the_last_group_loans": ...
}

error = {
	"command_unavailable_for_private": ...,
	"command_unavailable_for_group": ...,
	"amount_money_not_valid": ...,
	"waiting_for_all_users": ...,
	"lack_of_authorization(user)": ...,
	"user_unregistered(user)": ...,
	"can't_deauthorize_cause_not_authorized_yet": ...,
	"have_authorized_yet_this_user": ...,
	"maybe_you_wrote_an_username_instead_id": ...,
	"insert_a_correct_number": ...
}

# commands

private_commands = {
	...: "START",
	...: "COMMANDS",
	...: "AUTHORIZE",
	...: "DEAUTHORIZE",
	...: "GIVEN",
	...: "MYID",
	...: "BALANCE",
	...: "LAST_CHARGES",
	...: "LAST_LOANS",
	...: "GUIDE"
}

group_commands = {
	...: "SPENT",
	...: "SPENT", # version with @[language]_cembot

	...: "PRESENTATION",
	...: "PRESENTATION", # version with @[language]_cembot

	...: "LAST_GROUP_EXPENSES",
	...: "LAST_GROUP_EXPENSES", # version with @[language]_cembot
}
