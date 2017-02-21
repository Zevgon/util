from collections import deque
import sys
sys.path.append('..')
from functions import deep_dup

#Edges in this graph are from one position to all adjacent positions, not including diagonals.
class AdjacencyMatrixGraph:
	#passable_v_vals, targets, and obstacles must be passed in as sets
	def __init__(self, grid, passable_v_vals = None, targets = None, obstacles = None):
		if not grid:
			raise Exception('Grid cannot be empty')
		length = len(grid[0])
		if not length:
			raise Exception('Grid must have at least one element and must be rectangular')
		row_len = len(grid[0])
		if not all(len(x) == row_len for x in grid):
			raise Exception('Grid must be rectangular')

		if not passable_v_vals:
			passable_v_vals = set([0])
		if not targets:
			targets = set([1])
		if not obstacles:
			obstacles = set([2])
		self.passable_v_vals = passable_v_vals
		self.targets = targets
		self.obstacles = obstacles

		self.grid = grid
		self.num_vs = len(grid) * len(grid[0])
		self.rows = len(grid)
		self.cols = len(grid[0])

	def __all_passable_v_ids__(self):
		result = []
		for v_id in range(self.num_vs):
			i, j = self.__v_id_to_pos__(v_id)
			if self[[i, j]] in self.passable_v_vals:
				result.append(v_id)
		return result

	def __child_ids__(self, v_id):
		self.__validate_id__(v_id)
		pos = self.__v_id_to_pos__(v_id)
		i, j = pos
		child_poses = self.__child_poses__(i, j)
		result = []
		for pos in child_poses:
			i, j = pos
			result.append(self.__pos_to_v_id__(i, j))
		return result

	def __child_poses__(self, i, j):
		#N, E, S, W
		self.__validate_pos__(i, j)
		result = []
		if i != 0:
			result.append((i - 1, j))
		if j != self.cols - 1:
			result.append((i, j + 1))
		if i != self.rows - 1:
			result.append((i + 1, j))
		if j != 0:
			result.append((i, j - 1))
		return result

	def __compute_dists__(self):
		empty = []
		for i in range(self.num_vs):
			row = []
			for j in range(self.num_vs):
				row.append(float('inf'))
			empty.append(row)
		for parent_id in range(self.num_vs):
			if self.__val_by_id__(parent_id) in self.passable_v_vals:
				child_ids = self.__child_ids__(parent_id)
				for child_id in child_ids:
					if child_id not in self.obstacles:
						empty[parent_id][child_id] = 1
		return empty

	def __getitem__(self, pos):
		if type(pos) in [list, tuple]:
			self.__validate_pos__(pos[0], pos[1])
			return self.grid[pos[0]][pos[1]]
		else:
			if pos < 0 or pos >= len(self.grid):
				raise IndexError('Row index out of range')
			return self.grid[pos]

	def __setitem__(self, pos, val):
		self.__validate_pos__(pos[0], pos[1])
		self.grid[pos[0]][pos[1]] = val
		return val

	def __len__(self):
		return len(self.grid)

	def __passable_v_ids_and_targets__(self):
		passables = []
		targets = []
		for v_id in range(self.num_vs):
			i, j = self.__v_id_to_pos__(v_id)
			val = self[[i, j]]
			if val in self.passable_v_vals:
				passables.append(v_id)
			elif val in self.targets:
				targets.append(v_id)
		return [passables, targets]

	def __pos_to_v_id__(self, i, j):
		self.__validate_pos__(i, j)
		return i * self.cols + j

	def __val_by_id__(self, v_id):
		i, j = self.__v_id_to_pos__(v_id)
		return self[[i, j]]

	def __validate_id__(self, v_id):
		if v_id < 0 or v_id >= self.num_vs:
			raise Exception('Vertex ID out of range')

	def __validate_pos__(self, i, j):
		if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
			raise IndexError('Index out of range')

	def __v_id_to_pos__(self, v_id):
		self.__validate_id__(v_id)
		row_length = self.cols
		j = v_id % row_length
		v_id -= j
		i = v_id / row_length
		return [i, j]

	def floyd_warshall_distances_only(self):
		#Only returns minimum distances between all pairs of vertices, not paths
		passables, targets = self.__passable_v_ids_and_targets__()
		all_destinations = passables + targets
		dists = self.__compute_dists__()
		seen_vs = set()
		for through_v in passables:
			for v1 in passables:
				for v2 in all_destinations:
					total_through_dist = dists[v1][through_v] + dists[through_v][v2]
					if total_through_dist < dists[v1][v2]:
						dists[v1][v2] = total_through_dist
		return dists

	def dist_to_nearest_target(self, i, j):
		self.__validate_pos__(i, j)
		if self[[i, j]] not in self.passable_v_vals:
			raise Exception('Must start from an empty coordinate')
		q = deque([(i, j, 0)])
		visited = set()
		while q:
			cur_i, cur_j, dist = q.popleft()
			if self[[cur_i, cur_j]] in self.targets:
				return dist
			child_poses = self.__child_poses__(cur_i, cur_j)
			for pos in child_poses:
				if not pos in visited and self[pos] not in self.obstacles:
					q.append((pos[0], pos[1], dist + 1))
					visited.add(pos)
		return float('inf')

	def dists_from_all_targets(self):
		for i in range(len(self.grid)):
			for j in range(len(self.grid[0])):
				if self[[i, j]] in self.targets:
					self.dists_from_target(i, j)

	def dists_from_target(self, i, j):
		self.__validate_pos__(i, j)
		if self[[i, j]] not in self.targets:
			raise Exception('Must start from a target')
		q = deque([(i, j, 0)])
		visited = set()
		while q:
			cur_i, cur_j, dist = q.popleft()
			child_poses = self.__child_poses__(cur_i, cur_j)
			for pos in child_poses:
				cur_el = self[pos]
				if not pos in visited and cur_el not in self.obstacles and cur_el not in self.targets:
					self[pos] = min(self[pos], dist + 1)
					q.append((pos[0], pos[1], dist + 1))
					visited.add(pos)

	def dup_grid(self):
		return deep_dup(self.grid)

	def explore(self, i, j, seen):
		q = deque([(i, j)])
		while q:
			cur_i, cur_j = q.popleft()
			child_poses = self.__child_poses__(cur_i, cur_j)
			for pos in child_poses:
				if pos not in seen and self[pos] in self.targets:
					q.append(pos)
					seen.add(pos)

	def first(self):
		return self[[0, 0]]

	def last(self):
		i = len(self) - 1
		j = len(self[0]) - 1
		return self[[i, j]]

	def num_groups_of_targets(self):
		seen = set()
		result = 0
		for i in range(len(self.grid)):
			for j in range(len(self.grid[0])):
				if (i, j) in seen:
					continue
				elif self[[i, j]] in self.targets:
					result += 1
					self.explore(i, j, seen)
				seen.add((i, j))
		return result

	def total_dists_and_best_position_to_access_targets(self):
		dists = self.floyd_warshall_distances_only()
		passables, targets = self.__passable_v_ids_and_targets__()
		min_dist = float('inf')
		build_id = None
		for i in passables:
			total_dists_to_targets = 0
			for j in targets:
				total_dists_to_targets += dists[i][j]
			if total_dists_to_targets < min_dist:
				min_dist = total_dists_to_targets
				build_id = i
		pos = None
		if build_id:
			pos = self.__v_id_to_pos__(build_id)
		return [min_dist, pos]

	def shortest_distances_from_all_targets(self):
		from dists_from_targets import shortest_distances_from_all_targets
		return shortest_distances_from_all_targets(self)

	def shortest_dist_ball(self, start_pos, end_pos):
		from ball import shortest_dist_ball
		return shortest_dist_ball(self, start_pos, end_pos)

	def num_paths_from_top_left_to_bottom_right(self):
		if self.first() not in self.passable_v_vals or self.last() not in self.passable_v_vals:
			return 0
		grid = self.dup_grid()
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if self[[i, j]] in self.passable_v_vals:
					if i == 0 or j == 0:
						grid[i][j] = 1
					else:
						grid[i][j] = grid[i - 1][j] + grid[i][j - 1]
				else:
					grid[i][j] = 0
		return grid[len(grid) - 1][len(grid[0]) - 1]



# grid1 = [[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]
# mg1 = AdjacencyMatrixGraph(grid1)
# print mg1.total_dists_and_best_position_to_access_targets()

# grid2 = [[float('inf'), -1, 0, float('inf')], [float('inf'), float('inf'), float('inf'), -1], [float('inf'), -1, float('inf'), -1], [0, -1, float('inf'), float('inf')]]
# mg2 = AdjacencyMatrixGraph(grid2, set([float('inf')]), set([0]), set([-1]))
# mg2.dists_from_all_targets()
# print mg2.grid

# grid3 = [
#   '11000',
#   '11000',
#   '00100',
#   '00011'
# ]
# grid4 = [
#   '11110',
#   '11010',
#   '11000',
#   '00000'
# ]
# mg3 = AdjacencyMatrixGraph(grid4, set(['0']), set(['1']))
# print mg3.num_groups_of_targets()

# grid4 = [
#   [0, 0, 1, 0, 0],
#   [1, 0, 0, 1, 0],
#   [0, 0, 0, 0, 0],
#   [0, 1, 0, 1, 1],
#   [0, 0, 0, 1, 0]
# ]
# mg4 = AdjacencyMatrixGraph(grid4, set([0]), None, set([1]))
# print mg4.shortest_dist_ball([1, 2], [2, 4])


# grid5 = [
#   [0,2,0,2,2,0,2,2],
#   [0,2,2,2,1,0,1,2],
#   [0,0,0,1,0,2,0,0],
#   [2,0,0,2,0,2,2,0],
#   [0,0,0,2,0,0,0,0]
# ]
# mg5 = AdjacencyMatrixGraph(grid5)
# print mg5.shortest_distances_from_all_targets()


# grid6 = [
#   [0, 0, 0],
#   [0, 1, 1],
#   [0, 0, 0],
#   [0, 1, 0],
#   [0, 0, 0]
# ]
#
# mg6 = AdjacencyMatrixGraph(grid6)
# print mg6.num_paths_from_top_left_to_bottom_right()
