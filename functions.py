from collections import deque
from random import randint
import re

def deep_dup(l, q = False):
	if q:
		result = deque()
	else:
		result = []
	for item in l:
		if type(item) in [list, deque]:
			result.append(deep_dup(item, type(item) == deque))
		else:
			result.append(item)
	return result

def create_matrix(row_num, col_num, default_val = None):
	result = []
	while len(result) < row_num:
		row = []
		while len(row) < col_num:
			row.append(default_val)
		result.append(row)
	return result

def bsearch(l, item, left_bound = 0, right_bound = None):
	if not l:
		return False
	if right_bound == None:
		right_bound = len(l)
	if left_bound >= len(l) or (left_bound == right_bound and l[left_bound] != item):
		return False
	half = (left_bound + right_bound) / 2
	if l[half] == item:
		return True
	elif item < l[half]:
		right_bound = half
		return bsearch(l, item, left_bound, right_bound)
	else:
		left_bound = half + 1
		return bsearch(l, item, left_bound, right_bound)

def bsearch_without_len(l, item, lower_bound = 0, upper_bound = 1):
	if not l:
		return False
	if lower_bound == upper_bound:
		return False
	i = (lower_bound + upper_bound) / 2
	try:
		if l[i] == item:
			return True
		elif item < l[i]:
			return bsearch_without_len(l, item, lower_bound, i)
		else:
			diff = upper_bound - lower_bound
			return bsearch_without_len(l, item, i + 1, upper_bound + diff)
	except IndexError:
		return bsearch_without_len(l, item, lower_bound, i)

def strip(grid, right = True):
	result = []
	for row in grid:
		if right and row:
			result.append(row.pop())
		elif row:
			result.append(row.popleft())
	return result


def spiral_order(grid):
	result = []
	if not grid:
		return result
	row_len = len(grid[0])
	i = 1
	while i < len(grid):
		if len(grid[i]) != row_len:
			print 'Grid is not rectangular. Continue anyway?\n("y" for yes, anything else for no)\n>>',
			res = input()
			if res == 'y':
				break
			else:
				return []
		i += 1
	grid_dup = deque(map(lambda x: deque(x), grid))
	side = 0
	while grid_dup:
		if side == 4:
			side = 0
		if side == 0:
			result += grid_dup.popleft()
		elif side == 1:
			result += strip(grid_dup)
		elif side == 2:
			result += reversed(grid_dup.pop())
		else:
			result += reversed(strip(grid_dup, False))
		side += 1
	return result

def get_positions(grid, i, j):
	first = [i, j]
	second = [len(grid) - j - 1, i]
	third = [len(grid) - i - 1, len(grid) - j - 1]
	fourth = [j, len(grid) - i - 1]
	return [first, second, third, fourth]

def swap(grid, positions):
	first, second, third, fourth = positions
	top_left = grid[first[0]][first[1]]
	i = 0
	while i < len(positions) - 1:
		cur_pos = positions[i]
		next_pos = positions[i + 1]
		grid[cur_pos[0]][cur_pos[1]] = grid[next_pos[0]][next_pos[1]]
		i += 1
	grid[fourth[0]][fourth[1]] = top_left

def rotate_square_grid(grid):
	#Mutates grid
	if not grid:
		return grid
	row_len = len(grid[0])
	for row in grid:
		if len(row) != row_len:
			raise Exception('Grid is not square')
	for i in range(len(grid) / 2):
		for j in range(i, len(grid) - i - 1):
			four_positions = get_positions(grid, i, j)
			swap(grid, four_positions)

def valid_emails(strs):
	result = []
	for string in strs:
		if re.match('^[^@]+@[^.@]+\.[^.@]+$', string):
			result.append(string)
	return result

def valid_emails_no_regex(strs):
	result = []
	for string in strs:
		if not string or string.count('@') != 1:
			continue
		if string[0] == '@' or string[-1] == '@':
			continue
		right_side = string[string.index('@') + 1:]
		if right_side[0] == '.' or right_side[-1] == '.':
			continue
		if right_side.count('.') != 1:
			continue
		result.append(string)
	return result

def valid_email(string):
	if not string:
		return False
	if string[0] in ['@', '.'] or string[-1] in ['@', '.']:
		return False
	i = 0
	seen_at = False
	at_idx = None
	seen_dot = False
	while i < len(string):
		if string[i] == '@' and seen_at:
			return False
		elif string[i] == '@':
			seen_at = True
			at_idx = i
		if seen_at:
			if string[i] == '.' and seen_dot:
				return False
			elif string[i] == '.' and at_idx == i - 1:
				return False
			elif string[i] == '.':
				seen_dot = True
		i += 1
	return seen_at and seen_dot

def valid_emails_no_regex_2(strs):
	result = []
	for string in strs:
		if valid_email(string):
			result.append(string)
	return result

def find_emails(string):
	found = re.findall('[\b!?"\']*([^@!?\b]+@[^@.\b]+\.[^@.\b]+)', string)
	if found:
		return found
	else:
		return None

def shuffle_ip(l):
	count = len(l)
	idx = len(l) - 1
	while count:
		sample_idx = randint(0, count - 1)
		l[idx], l[sample_idx] = l[sample_idx], l[idx]
		idx -= 1
		count -= 1
