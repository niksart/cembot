def is_username(s):
	return len(s) - 1 > 4 and s[0] == "@"

def stringify(list_of_words):
	ret = ""
	first_word = True
	for word in list_of_words:
		if first_word:
			ret = word
			first_word = False
		else:
			ret = ret + ' ' + word
	return ret
