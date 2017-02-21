from collections import deque

def shortest_dist_ball(self, start_pos, end_pos):
	#Finds the shortest distance from a ball to a target, where the ball can only roll forwards until it hits a wall or obstacle, at which point it can decide which direction to turn. The ball must stop at the target, i.e. there must be a wall behind the target when the ball hits it.
	start_pos += [None, 0]
	start_pos = tuple(start_pos)
	seen = set()
	q = deque([start_pos])
	directions = ['N', 'E', 'S', 'W']
	while q:
		i, j, direction, dist = q.popleft()
		if [i, j] == end_pos:
			if not direction:
				return 0
			elif direction == 'N':
				if i == 0 or self[[i - 1, j]] in self.obstacles:
					return dist
			elif direction == 'E':
				if j == len(self.grid[0]) - 1 or self[[i, j + 1]] in self.obstacles:
					return dist
			elif direction == 'S':
				if i == len(self.grid) - 1 or self[[i + 1, j]] in self.obstacles:
					return dist
			elif direction == 'W':
				if j == 0 or self[[i, j - 1]] in self.obstacles:
					return dist
		if not direction:
			if i != 0 and self[[i - 1, j]] not in self.obstacles:
				q.append((i - 1, j, 'N', dist + 1))
				seen.add((i - 1, j, 'N'))
			if j != 0 and self[[i, j - 1]] not in self.obstacles:
				q.append((i, j - 1, 'W', dist + 1))
				seen.add((i, j - 1, 'W'))
			if i != len(self.grid) - 1 and self[[i + 1, j]] not in self.obstacles:
				q.append((i + 1, j, 'S', dist + 1))
				seen.add((i + 1, j, 'S'))
			if j != len(self.grid[0]) - 1 and self[[i, j + 1]] not in self.obstacles:
				q.append((i, j + 1, 'E', dist + 1))
				seen.add((i, j + 1, 'E'))
		elif direction == 'N':
			if i == 0 or self[[i - 1, j]] in self.obstacles:
				if j != 0 and (i, j - 1, 'W') not in seen and self[[i, j - 1]] not in self.obstacles:
					q.append((i, j - 1, 'W', dist + 1))
					seen.add((i, j - 1, 'W'))
				if j != len(self.grid[0]) - 1 and (i, j + 1, 'E') not in seen and self[[i, j + 1]] not in self.obstacles:
					q.append((i, j + 1, 'E', dist + 1))
					seen.add((i, j + 1, 'E'))
			else:
				q.append((i - 1, j, 'N', dist + 1))
				seen.add((i - 1, j, 'N'))
		elif direction == 'E':
			if j == len(self.grid[0]) - 1 or self[[i, j + 1]] in self.obstacles:
				if i != 0 and (i - 1, j, 'N') not in seen and self[[i - 1, j]] not in self.obstacles:
					q.append((i - 1, j, 'N', dist + 1))
					seen.add((i - 1, j, 'N'))
				if i != len(self.grid) - 1 and (i + 1, j, 'S') not in seen and self[[i + 1, j]] not in self.obstacles:
					q.append((i + 1, j, 'S', dist + 1))
					seen.add((i + 1, j, 'S'))
			else:
				q.append((i, j + 1, 'E', dist + 1))
				seen.add((i, j + 1, 'E'))
		elif direction == 'S':
			if i == len(self.grid) - 1 or self[[i + 1, j]] in self.obstacles:
				if j != len(self.grid[0]) - 1 and (i, j + 1, 'E') not in seen and self[[i, j + 1]] not in self.obstacles:
					q.append((i, j + 1, 'E', dist + 1))
					seen.add((i, j + 1, 'E'))
				if j != 0 and (i, j - 1, 'W') not in seen and self[[i, j - 1]] not in self.obstacles:
					q.append((i, j - 1, 'W', dist + 1))
					seen.add((i, j - 1, 'W'))
			else:
				q.append((i + 1, j, 'S', dist + 1))
				seen.add((i + 1, j, 'S'))
		elif direction == 'W':
			if j == 0 or self[[i, j - 1]] in self.obstacles:
				if i != 0 and (i - 1, j, 'N') not in seen and self[[i - 1, j]] not in self.obstacles:
					q.append((i - 1, j, 'N', dist + 1))
					seen.add((i - 1, j, 'N'))
				if i != len(self.grid) - 1 and (i + 1, j, 'S') not in seen and self[[i + 1, j]] not in self.obstacles:
					q.append((i + 1, j, 'S', dist + 1))
					seen.add((i + 1, j, 'S'))
			else:
				q.append((i, j - 1, 'W', dist + 1))
				seen.add((i, j - 1, 'W'))
	return -1
