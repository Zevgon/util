from random import randint

def random_characters_generator(min_length, max_length, char_options = None):
	if not char_options:
		char_options = list(range(48, 57)) + list(range(65, 90)) + list(range(97, 122))
		char_options = list(map(lambda x: chr(x), char_options))
	length = randint(min_length, max_length)
	s = ''
	while len(s) < length:
		idx = randint(0, len(char_options) - 1)
		s += char_options[idx]
	return s

# print random_characters_generator(4, 4, ['W', '0', 'E'])

#longest word in './dictionary.txt' = 'electroencephalographic' (23 chars)
def random_words_generator(min_length, max_length, words = None):
	if not words:
		f = open('dictionary.txt')
		words = list(map(lambda x: x.strip(), f.readlines()))
	list_length = randint(min_length, max_length)
	l = []
	while len(l) < list_length:
		idx = randint(0, len(words) - 1)
		l.append(words[idx])
	return l

def random_list_generator(min_list_length = 0, max_list_length = 1000, min_el_length = 0, max_el_length = 20, char_options = None):
	if not char_options:
		char_options = list(range(48, 57)) + list(range(65, 90)) + list(range(97, 122))
		char_options = list(map(lambda x: chr(x), char_options))
	elif char_options == 'letters':
		char_options = list(range(65, 90)) + list(range(97, 122))
		char_options = list(map(lambda x: chr(x), char_options))
	elif char_options == 'lowercase letters':
		char_options = list(range(97, 122))
		char_options = list(map(lambda x: chr(x), char_options))
	list_length = randint(min_list_length, max_list_length)
	l = []
	while len(l) < list_length:
		l.append(random_characters_generator(min_el_length, max_el_length, char_options))
	return l

def random_matrix_generator(min_rows, max_rows, min_cols, max_cols, el_options = None):
	if type(el_options) == range:
		el_options = list(el_options)
	if not el_options:
		el_options = list(range(48, 57)) + list(range(65, 90)) + list(range(97, 122))
		el_options = list(map(lambda x: chr(x), el_options))
	result = []
	rows = randint(min_rows, max_rows)
	cols = randint(min_cols, max_cols)
	while len(result) < rows:
		row = []
		while len(row) < cols:
			idx = randint(0, len(el_options) - 1)
			el = el_options[idx]
			row.append(el)
		result.append(row)
	return result

def random_int_list_generator(min_len, max_len, ran = None):
	if not ran:
		ran = [0, 2 ** 8]
	length = randint(min_len, max_len)
	result = []
	while len(result) < length:
		result.append(randint(ran[0], ran[1]))
	return result

# print random_list_generator(4000, 4000, 2, 5, 'lowercase letters')
# a = random_matrix_generator(2000, 2000, 2, 2, range(0, 100))
# a = list(map(lambda x: tuple(x), a))
# a = list(set(a))
# a = list(map(lambda x: list(x), a))
# print a

def random_transaction_generator(num_transactions, num_people, max_amt):
	result = []
	while len(result) < num_transactions:
		person1 = randint(0, num_people - 1)
		person2 = randint(0, num_people - 1)
		amt = randint(1, max_amt)
		result.append([person1, person2, amt])
	return result

print random_transaction_generator(300, 8, 10)
