from collections import deque

def get_target_poses(self):
	result = []
	for i in range(len(self)):
		for j in range(len(self[0])):
			if self[[i, j]] in self.targets:
				result.append([i, j])
	return result

def create_dist_map(self):
	result = []
	for i in range(len(self)):
		row = []
		for j in range(len(self[0])):
			row.append([0, 0])
		result.append(row)
	return result

def bfs_and_mutate(self, dist_map, pos, num_targets):
	pos = tuple(pos)
	q = deque([[pos, 0]])
	visited = set([pos])
	ones_seen = 0
	zeroes_seen = 0
	while q:
		# print q
		cur_pos, dist = q.popleft()
		i, j = cur_pos
		adjes = self.__child_poses__(i, j)
		for adj in adjes:
			if adj in visited:
				continue
			adj_i, adj_j = adj
			if self[adj] == 0:
				zeroes_seen += 1
				dist_map[adj_i][adj_j][0] += dist + 1
				dist_map[adj_i][adj_j][1] += 1
				q.append([[adj_i, adj_j], dist + 1])
			elif self[adj] == 1:
				ones_seen += 1
			visited.add((adj_i, adj_j))
	possible = ones_seen == num_targets - 1 and zeroes_seen > 0
	if not possible:
		return False
	return True

def find_min_dist(dist_map, num_targets):
	minimum = float('inf')
	for i in range(len(dist_map)):
		for j in range(len(dist_map[0])):
			if dist_map[i][j][1] == num_targets:
				minimum = min(minimum, dist_map[i][j][0])
	if minimum == float('inf'):
		return -1
	return minimum

def shortest_distances_from_all_targets(self):
	target_poses = get_target_poses(self)
	if not target_poses:
		return -1
	num_targets = len(target_poses)
	dists = create_dist_map(self)
	while target_poses:
		cur_pos = target_poses.pop()
		possible = bfs_and_mutate(self, dists, cur_pos, num_targets)
		if not possible:
			return -1
	return find_min_dist(dists, num_targets)
