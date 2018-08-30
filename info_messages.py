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

IT = {
	"start": "Sei stanco di doverti ricordare a chi devi soldi o chi te li deve?\nNessun problema, da oggi ci sono io, Cembot: il tuo libro contabile!📖\n\n"
			 "Sono utile principalmente per ricordare debiti e crediti che hai nei confronti delle persone che mi usano. Ti aiuterò ad amministrare le spese sia tra singole persone che all'interno di gruppi di persone. Per usarmi più facilmente imposta un username (Impostazioni ➡️ username).\n\n"
			 "Ora che sei in chat privata, quello che puoi fare è:\n"
			 "1️⃣ approvare o revocare l'autorizzazione di un utente ad addebitare sul tuo conto con i comandi /autorizza o /revoca\n"
			 "2️⃣ addebitare sul conto di un utente una spesa con il comando /dato (l'utente deve averti autorizzato). Per esempio, \"/dato 6.50 @luca pizza margherita\" se ieri sera hai prestato i soldi per la pizza a Luca\n"
			 "3️⃣ ottenere il tuo id, necessario solo se non hai ancora impostato un username, con il comando /mioid\n"
			 "4️⃣ visualizzare il bilancio verso tutti o verso un particolare utente con il comando /bilancio\n\n"
		     "Se provi ad aggiungermi ad un gruppo, lavorerò in modo diverso: ogni spesa aggiunta da un partecipante verrà ripartita equamente tra tutti i componenti del gruppo. Prendiamo ad esempio il gruppo \"Festone\" composto da Mario, Gianluca e Marta. Se Marta compra la torta e spende 30 euro, questi soldi verranno ripartiti in tre: Mario avrà un debito verso Marta di 10 euro, così come Gianluca.\n"
			 "Ecco quello che è possibile farmi fare in un gruppo:\n"
			 "1️⃣ aggiungere una spesa (la torta di prima per esempio) con il comando /speso\n"
			 "2️⃣ presentarsi a me (ho bisogno di conoscere gli appartenenti al gruppo prima che entrassi)\n\n"
			 "Comincia a esplorare le mie potenzialità! 😎 \nUsa il comando /comandi per ottenere la descrizione completa dei comandi!",
	"introduced_in_group": "Buongiorno, piacere Cembot! 🤙🏼\nPer cominciare, ho bisogno che ogni partecipante che era dentro al gruppo prima che arrivassi si presenti.\n"
	                       "Le persone aggiunte dopo questo messaggio possono fare a meno di presentarsi. Da ora infatti, terrò traccia di chi entra ed esce dal gruppo.\n"
	                       "Presentati con il comando /presente!",
	"each_member_introduced": "Ok perfetto! Ogni membro si è introdotto!\nOra possiamo partire!",
	"person_missing": "Manca una persona all'appello.",
	"people_missing": " persone mancano all'appello.",

	"transaction_succeed": "Transazione aggiunta correttamente!",

	"authorized_confirm(user)": "L'utente @%s è stato autorizzato a caricarti debiti.",
	"deauthorized_confirm(user)": "L'utente @%s è stato deautorizzato, non potrà più caricarti debiti.",
	"your_id_is(id)": "Il tuo id Telegram è %s. Puoi impostare un username dalle impostazioni Telegram per usare Cembot più facilmente.",
	"balance_with_other_user(user,balance)": "Il tuo bilancio nei confronti di %s è %s.",
	"header_balance_credit": "📗 Crediti\n",
	"header_balance_debit": "📕 Debiti\n",
	"commands": "🔽 /start\nMostra il messaggio introduttivo a Cembot.\n\n"
				"🔽 /comandi\nMostra questo messaggio.\n\n"
				"🔽 /autorizza \nAutorizza un utente ad addebitarti spese.\nModalità d'uso alternative:\n▪️ /autorizza @<username>\n▪️ /autorizza <id utente>\n\n"
				"🔽 /revoca\nRevoca l'autorizzazione di un utente. Non potrà più addebitarti spese. \nModalità d'uso alternative:\n▪️ /revoca @<username>\n▪️ /revoca <id utente>\n\n"
				"🔽 /dato️\nPresta dei soldi ad un tuo amico.\nModalità d'uso alternative:\n▪️ /dato <soldi> @<username> <descrizione>\n▪️ /dato <soldi> <user id> <descrizione>\nPer esempio, scrivi \"/dato 6.50 @luca pizza margherita\" se ieri sera hai prestato i soldi per la pizza a Luca.\n\n"
				"🔽 /mioid\nOttieni il tuo ID Telegram. Se non hai ancora impostato uno username, puoi usare l'ID al suo posto.\n\n"
				"🔽 /bilancio \nOttieni la lista di debiti e crediti nei confronti degli utenti con i quali sei entrato in contatto. Scrivendo il nome utente dopo il comando ti verrà restituito il saldo verso quell'utente.\nModalità d'uso alternative:\n▪️ /bilancio\n▪️ /bilancio @<username>\n\n"
				"🔽 /speso\nUsa questo comando all'interno di un gruppo se vuoi dividere la spesa fra tutti i partecipanti al gruppo, compreso te stesso.\nModalità d'uso:\n▪️ /speso <soldi> <descrizione>.\n\n"
}