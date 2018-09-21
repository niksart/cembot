# Support for italian (IT) language

helper_commands = {
	"AUTHORIZE": "Usa questo comando se vuoi autorizzare un utente.\n"
	             "Modalità d'uso alternative:\n"
	             "▪️ /autorizza @<username>\n"
	             "▪️ /autorizza <id utente>",
	"DEAUTHORIZE": "Usa questo comando se vuoi revocare l'autorizzazione ad un utente.\n"
	               "Modalità d'uso alternative:\n"
	               "▪️ /revoca @<username>\n"
	               "▪️ /revoca <id utente>",
	"GIVEN": "Usa questo comando se hai prestato dei soldi a un tuo amico.\n"
	         "Modalità d'uso alternative:\n"
	         "▪️ /dato <soldi> @<username> <descrizione>\n"
	         "▪️ /dato <soldi> <user id> <descrizione>",
	"SPENT": "Usa questo comando all'interno di un gruppo se vuoi dividere la spesa fra tutti i partecipanti al gruppo, compreso te stesso.\n"
	         "Modalità d'uso:\n"
	         "▪️ /speso <soldi> <descrizione>.",
	"MYID": "Uso:\n"
	        "/mioid\n"
	        "Ottieni il tuo id Telegram se non hai settato l'username.",
	"START": "Uso:\n"
	         "/start\n"
	         "Mostra il messaggio iniziale.",
	"LAST_GROUP_EXPENSES": "Usa questo comando in un gruppo per vedere le ultime spese effettuate. \n"
	                       "Modalità d'uso alternative:\n"
	                       "▪️ /ultime_spese (mostra max 5 spese)\n"
	                       "▪️ /ultime_spese <n max spese da mostrare>",
	"LAST_CHARGES": "Usa questo comando in un chat privata per vedere gli ultimi addebiti sul tuo conto. \n"
	                "Modalità d'uso alternative:\n"
	                "▪️ /ultimi_addebiti (mostra max 5 addebiti)\n"
	                "▪️ /ultimi_addebiti <n max addebiti da mostrare>",
	"LAST_LOANS": "Usa questo comando in chat privata per vedere gli ultimi prestiti fatti. \n"
	              "Modalità d'uso alternative:\n"
	              "▪️ /ultimi_prestiti (mostra max 5 prestiti)\n"
	              "▪️ /ultimi_prestiti <n max prestiti da mostrare>"
}

info = {
	"start": "Sei stanco di doverti ricordare a chi devi soldi o chi te li deve?\n"
	         "Nessun problema, da oggi ci sono io, Cembot: il tuo libro contabile!📖\n\n"
			 "Ti aiuterò ad amministrare le spese sia tra singole persone che all'interno di gruppi di persone. \n\n"
	         "Entra subito nel mondo di Cembot! ✌\n\n"
	         "Vai alla /guida ▶️",
	"guide": "Benvenuto nella guida di Cembot! 📖\n\n"
			 "Per usarmi più facilmente imposta un username (Impostazioni ➡️ username).\n\n"
			 "Ora che sei in chat privata, quello che puoi fare è:\n"
			 "1️⃣ approvare o revocare l'autorizzazione di un utente ad addebitare sul tuo conto con i comandi /autorizza o /revoca\n"
			 "2️⃣ addebitare sul conto di un utente una spesa con il comando /dato (l'utente deve averti autorizzato). Per esempio, \"/dato 6.50 @luca pizza margherita\" se ieri sera hai prestato i soldi per la pizza a Luca\n"
			 "3️⃣ ottenere il tuo id, necessario solo se non hai ancora impostato un username, con il comando /mioid\n"
			 "4️⃣ visualizzare il bilancio verso tutti o verso un particolare utente con il comando /bilancio\n\n"
		     "Se provi ad aggiungermi ad un gruppo, lavorerò in modo diverso: ogni spesa aggiunta da un partecipante verrà ripartita equamente tra tutti i componenti del gruppo. Prendiamo ad esempio il gruppo \"Festone\" composto da Mario, Gianluca e Marta. Se Marta compra la torta e spende 30 euro, questi soldi verranno ripartiti in tre: Mario avrà un debito verso Marta di 10 euro, così come Gianluca.\n"
			 "Ecco quello che è possibile farmi fare in un gruppo:\n"
			 "1️⃣ aggiungere una spesa (la torta di prima per esempio) con il comando /speso\n"
			 "2️⃣ presentarsi a me (ho bisogno di conoscere gli appartenenti al gruppo prima che entrassi)\n\n"
			 "Comincia a esplorare le mie potenzialità! 😎 \n"
	         "Usa il comando /comandi per ottenere la descrizione completa dei comandi!",
	"introduced_in_group": "Buongiorno, piacere Cembot! 🤙🏼\n"
	                       "Per cominciare, ho bisogno che ogni partecipante che era dentro al gruppo prima che arrivassi si presenti.\n"
	                       "Le persone aggiunte dopo questo messaggio possono fare a meno di presentarsi. Da ora infatti, terrò traccia di chi entra ed esce dal gruppo.\n"
	                       "Presentati con il comando /presente!",
	"each_member_introduced": "Ok perfetto! Ogni membro si è introdotto!\n"
	                          "Ora possiamo partire!",
	"person_missing": "Manca una persona all'appello.",
	"people_missing": " persone mancano all'appello.",

	"transaction_succeed": "Transazione aggiunta correttamente!",

	"authorized_confirm(user)": "L'utente @%s è stato autorizzato a caricarti debiti.",
	"deauthorized_confirm(user)": "L'utente @%s è stato deautorizzato, non potrà più caricarti debiti.",
	"your_id_is(id)": "Il tuo id Telegram è %s. Puoi impostare un username dalle impostazioni Telegram per usare Cembot più facilmente.",
	"balance_with_other_user(user,balance)": "Il tuo bilancio nei confronti di %s è %s.",
	"header_balance_credit": "📗 Crediti\n",
	"header_balance_debit": "📕 Debiti\n",
	"commands": "🔽 /start\n"
	            "Mostra il messaggio introduttivo a Cembot.\n\n"
	            
	            "🔽 /guida\n"
	            "Mostra la guida di Cembot.\n\n"
				
				"🔽 /comandi\n"
	            "Mostra questo messaggio.\n\n"
				
				"🔽 /autorizza \n"
	            "Autorizza un utente ad addebitarti spese.\n"
	            "Modalità d'uso alternative:\n"
	            "▪️ /autorizza @<username>\n"
	            "▪️ /autorizza <id utente>\n\n"
				
				"🔽 /revoca\n"
	            "Revoca l'autorizzazione di un utente. Non potrà più addebitarti spese. \n"
	            "Modalità d'uso alternative:\n"
	            "▪️ /revoca @<username>\n"
	            "▪️ /revoca <id utente>\n\n"
	            
				"🔽 /dato️\n"
	            "Presta dei soldi ad un tuo amico.\n"
	            "Modalità d'uso alternative:\n"
	            "▪️ /dato <soldi> @<username> <descrizione>\n"
	            "▪️ /dato <soldi> <user id> <descrizione>\n"
	            "Per esempio, scrivi \"/dato 6.50 @luca pizza margherita\" se ieri sera hai prestato i soldi per la pizza a Luca.\n\n"
				
				"🔽 /mioid\n"
	            "Ottieni il tuo ID Telegram. Se non hai ancora impostato uno username, puoi usare l'ID al suo posto.\n\n"
				
				"🔽 /bilancio \n"
	            "Ottieni la lista di debiti e crediti nei confronti degli utenti con i quali sei entrato in contatto. Scrivendo il nome utente dopo il comando ti verrà restituito il saldo verso quell'utente.\n"
	            "Modalità d'uso alternative:\n"
	            "▪️ /bilancio\n"
	            "▪️ /bilancio @<username>\n\n"
				
				"🔽 /speso\n"
	            "Usa questo comando all'interno di un gruppo se vuoi dividere la spesa fra tutti i partecipanti al gruppo, compreso te stesso.\n"
	            "Modalità d'uso:\n"
	            "▪️ /speso <soldi> <descrizione>.\n\n"
				
				"🔽 /ultime_spese\n"
	            "Usa questo comando all'interno di un gruppo per conoscere le ultime spese fatte nel gruppo.\n"
	            "Modalità d'uso:\n"
	            "▪️ /ultime_spese (mostra max 10 spese)\n"
	            "▪️ /ultime_spese <n max spese>\n\n"
				
				"🔽 /ultimi_addebiti\n"
	            "Usa questo comando in chat privata con Cembot per conoscere gli ultimi addebiti sul tuo conto sia da parte di utenti che di gruppi.\n"
	            "Modalità d'uso:\n"
	            "▪️ /ultimi_addebiti (mostra max 10 addebiti)\n"
	            "▪️ /ultimi_addebiti <n max addebiti>\n\n"
				
				"🔽 /ultimi_prestiti\n"
	            "Usa questo comando in chat privata con Cembot per conoscere gli ultimi prestiti che hai fatto a utenti o gruppi.\n"
	            "Modalità d'uso:\n"
	            "▪️ /ultimi_prestiti (mostra max 10 prestiti)\n"
	            "▪️ /ultimi_prestiti <n max prestiti>\n\n",
	"these_are_the_last_group_expenses": "Ecco le ultime spese di questo gruppo (la prima è l'ultima spesa inserita):\n\n",
	"these_are_the_last_individual_charges": "Ecco gli ultimi addebiti fatti da utenti individuali sul tuo conto (pagante, importo, descrizione):\n\n",
	"these_are_the_last_group_charges": "Ecco gli ultimi addebiti fatti dai gruppi sul tuo conto (pagante, nome del gruppo, importo, descrizione):\n\n",
	"no_charges_yet": "Non hai ancora nessun addebito!",
	"these_are_the_last_individual_loans": "Ecco i tuoi ultimi prestiti verso un utente (beneficiario, importo, descrizione):\n\n",
	"these_are_the_last_group_loans": "Ecco i tuoi ultimi prestiti verso un gruppo (nome gruppo beneficiario, importo, descrizione):\n\n"
}

error = {
	"command_unavailable_for_private": "Per usare questo comando apri una chat privata con @it_cembot.",
	"command_unavailable_for_group": "Per usare questo comando inserisci @it_cembot in un gruppo.",
	"amount_money_not_valid": "Quantità di soldi non valida.",

	"waiting_for_all_users": "Non tutti gli utenti si sono presentati.\nPresentatevi con /presente prima di aggiungere spese.",
    "lack_of_authorization(user)": "L'utente @%s non ti ha autorizzato a caricare spese sul suo conto. Contattalo per farti autorizzare.",
	"user_unregistered(user)": "L'utente @%s non è registrato nel nostro sistema.",
	"can't_deauthorize_cause_not_authorized_yet": "Non hai già autorizzato questo utente. Dunque non puoi revocarne l'autorizzazione.",
	"have_authorized_yet_this_user": "Hai già autorizzato questo utente.",
	"maybe_you_wrote_an_username_instead_id": "Questo non è un id numerico. Se intendevi scrivere un username scrivilo con la @ davanti.",
	"insert_a_correct_number": "Inserisci un numero corretto e riprova."
}

# commands

private_commands = {
	"start": "START",
    "comandi": "COMMANDS",
    "autorizza": "AUTHORIZE",
    "revoca": "DEAUTHORIZE",
	"dato": "GIVEN",
	"mioid": "MYID",
	"bilancio": "BALANCE",
	"ultimi_addebiti": "LAST_CHARGES",
	"ultimi_prestiti": "LAST_LOANS",
	"guida": "GUIDE"
}

group_commands = {
	"speso": "SPENT",
	"speso@it_cembot": "SPENT",

	"presente": "PRESENTATION",
	"presente@it_cembot": "PRESENTATION",

	"ultime_spese": "LAST_GROUP_EXPENSES",
	"ultime_spese@it_cembot": "LAST_GROUP_EXPENSES"
}
