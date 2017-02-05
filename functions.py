from collections import deque

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
