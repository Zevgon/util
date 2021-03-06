from collections import deque

class Node:
	def __init__(self, val):
		self.val = val
		self.oes = []
		self.ies = []
		self.net = 0

class Edge:
	def __init__(self, v1, v2, weight):
		self.weight = weight
		self.v1 = v1
		self.v2 = v2
		self.add_self_to_vertices()

	def add_self_to_vertices(self):
		self.v1.oes.append(self)
		self.v2.ies.append(self)

class Graph:
	def __init__(self):
		self.vs = {}
		self.non_zero_nets = 0

	def add_transaction(self, transaction):
		v1_id, v2_id, amt = transaction
		if v1_id in self.vs:
			v1 = self.vs[v1_id]
		else:
			v1 = Node(v1_id)
			self.vs[v1_id] = v1
		if v2_id in self.vs:
			v2 = self.vs[v2_id]
		else:
			v2 = Node(v2_id)
			self.vs[v2_id] = v2
			v2_seen_before = False
		Edge(v1, v2, amt)
		if amt != 0:
			self.update_nets(v1, v2, amt)

	def update_nets(self, v1, v2, amt):
		if v1.net == 0:
			self.non_zero_nets += 1
		if v2.net == 0:
			self.non_zero_nets += 1
		v1.net -= amt
		v2.net += amt
		if v1.net == 0:
			self.non_zero_nets -= 1
		if v2.net == 0:
			self.non_zero_nets -= 1

	def add_relationship(self, v1_id, v2_id, div):
		if v1_id in self.vs:
			v1 = self.vs[v1_id]
		else:
			v1 = Node(v1_id)
			self.vs[v1_id] = v1
		if v2_id in self.vs:
			v2 = self.vs[v2_id]
		else:
			v2 = Node(v2_id)
			self.vs[v2_id] = v2
		Edge(v1, v2, float(div))
		Edge(v2, v1, 1.0 / div)

	def get_relationship(self, v1_id, v2_id):
		if v1_id not in self.vs or v2_id not in self.vs:
			return -1
		q = deque([(self.vs[v1_id], 1.0)])
		seen = set()
		count = 0
		while q:
			cur_v, ratio = q.popleft()
			for oe in cur_v.oes:
				if oe.v2.val == v2_id:
					answer = ratio * oe.weight
					if count > 0:
						Edge(self.vs[v1_id], self.vs[v2_id], answer)
						Edge(self.vs[v1_id], self.vs[v2_id], 1.0 / answer)
					return answer
				if oe.v2 not in seen:
					q.append((oe.v2, ratio * oe.weight))
					seen.add(oe.v2)
			seen.add(cur_v)
			count += 1
		return -1

# g = Graph()
# transactions = [[7, 3, 6], [3, 1, 4], [1, 6, 10], [4, 1, 8], [1, 7, 2], [6, 5, 4], [7, 4, 10], [0, 3, 1], [5, 4, 2], [3, 0, 8], [5, 2, 4], [7, 7, 6], [3, 2, 10], [1, 6, 4], [2, 2, 9], [6, 1, 1], [5, 3, 9], [2, 6, 9], [1, 3, 1], [5, 5, 1], [0, 5, 9], [2, 7, 10], [1, 5, 6], [6, 4, 7], [5, 3, 4], [3, 3, 7], [7, 6, 4], [2, 6, 7], [6, 7, 4], [0, 3, 5], [7, 4, 8], [4, 0, 10], [2, 1, 8], [4, 2, 10], [4, 4, 9], [5, 1, 4], [6, 5, 9], [4, 1, 8], [6, 1, 7], [4, 2, 2], [6, 2, 8], [6, 6, 9], [3, 3, 6], [5, 7, 2], [5, 5, 6], [3, 7, 9], [5, 0, 9], [2, 5, 3], [0, 2, 2], [2, 0, 3], [1, 4, 5], [1, 3, 10], [4, 0, 9], [6, 2, 2], [7, 2, 9], [4, 4, 8], [0, 0, 7], [7, 5, 3], [3, 6, 7], [6, 3, 5], [4, 1, 2], [3, 4, 2], [4, 4, 5], [4, 6, 4], [5, 1, 9], [4, 4, 5], [1, 1, 10], [0, 0, 7], [2, 0, 3], [0, 0, 6], [5, 5, 7], [4, 4, 8], [4, 3, 4], [7, 3, 10], [6, 2, 4], [3, 2, 2], [0, 6, 6], [4, 5, 5], [7, 3, 5], [0, 7, 1], [6, 3, 10], [5, 7, 4], [6, 0, 1], [3, 5, 3], [7, 7, 10], [4, 6, 7], [7, 0, 4], [0, 3, 10], [1, 1, 4], [7, 3, 3], [4, 7, 10], [1, 6, 9], [1, 0, 1], [1, 7, 9], [6, 1, 9], [5, 1, 4], [2, 5, 6], [0, 6, 10], [5, 3, 8], [4, 5, 8], [0, 2, 9], [5, 4, 6], [4, 0, 10], [0, 4, 1], [5, 6, 8], [7, 5, 10], [2, 4, 5], [1, 6, 5], [5, 4, 6], [2, 0, 10], [5, 2, 10], [4, 7, 5], [7, 2, 8], [1, 2, 7], [6, 5, 5], [4, 5, 2], [1, 4, 4], [3, 6, 6], [0, 6, 6], [7, 5, 1], [0, 6, 9], [2, 5, 6], [0, 0, 4], [5, 7, 6], [0, 2, 10], [6, 1, 7], [3, 5, 9], [6, 5, 10], [5, 5, 1], [1, 4, 1], [2, 5, 2], [2, 3, 9], [1, 3, 5], [6, 4, 3], [2, 1, 7], [2, 1, 8], [6, 2, 5], [7, 6, 4], [2, 4, 3], [1, 6, 7], [0, 4, 9], [0, 5, 10], [1, 6, 4], [4, 4, 8], [4, 0, 5], [3, 4, 2], [5, 2, 9], [2, 0, 2], [4, 2, 1], [1, 0, 7], [5, 5, 8], [0, 2, 8], [3, 5, 3], [3, 1, 10], [1, 3, 5], [7, 6, 8], [5, 7, 9], [6, 3, 5], [1, 0, 8], [0, 4, 6], [1, 2, 3], [6, 2, 1], [0, 7, 7], [2, 4, 3], [3, 3, 7], [5, 4, 1], [3, 3, 9], [5, 7, 1], [2, 2, 5], [7, 4, 4], [7, 1, 3], [2, 0, 8], [5, 7, 10], [5, 7, 6], [7, 3, 10], [4, 4, 7], [5, 2, 4], [5, 5, 9], [6, 4, 5], [3, 3, 6], [2, 2, 2], [0, 2, 8], [1, 3, 2], [4, 5, 9], [0, 1, 5], [5, 5, 9], [5, 7, 8], [3, 2, 3], [2, 0, 2], [2, 7, 4], [6, 7, 5], [1, 2, 4], [4, 3, 8], [6, 3, 4], [6, 7, 2], [4, 3, 2], [3, 6, 8], [0, 2, 2], [6, 6, 4], [0, 3, 7], [1, 2, 6], [6, 4, 1], [6, 4, 3], [4, 5, 6], [1, 6, 6], [6, 4, 6], [7, 7, 6], [1, 5, 10], [4, 5, 2], [2, 3, 2], [2, 4, 4], [4, 1, 8], [0, 3, 9], [6, 5, 2], [7, 2, 3], [2, 3, 4], [1, 0, 7], [4, 7, 2], [7, 5, 4], [6, 6, 10], [6, 6, 5], [6, 5, 7], [6, 4, 8], [6, 4, 5], [7, 3, 9], [4, 2, 2], [5, 0, 10], [5, 3, 2], [0, 3, 3], [0, 7, 1], [0, 7, 3], [3, 6, 4], [5, 3, 9], [1, 3, 4], [6, 3, 5], [0, 3, 6], [6, 3, 5], [2, 6, 9], [7, 6, 2], [0, 4, 3], [0, 5, 4], [6, 4, 1], [3, 2, 1], [7, 5, 1], [3, 0, 3], [7, 6, 7], [3, 2, 9], [5, 5, 3], [5, 5, 3], [0, 7, 8], [4, 4, 1], [2, 7, 3], [4, 1, 2], [3, 2, 8], [5, 6, 3], [1, 0, 8], [7, 6, 4], [1, 1, 8], [5, 0, 9], [0, 2, 3], [1, 0, 6], [1, 1, 3], [4, 2, 1], [0, 7, 1], [4, 1, 10], [1, 1, 4], [5, 7, 3], [4, 4, 7], [5, 3, 8], [3, 0, 6], [0, 0, 7], [6, 4, 8], [3, 7, 9], [2, 3, 2], [4, 4, 1], [3, 0, 4], [3, 2, 5], [0, 7, 8], [4, 2, 5], [6, 5, 3], [1, 0, 4], [6, 4, 3], [4, 5, 7], [7, 2, 4], [3, 2, 10], [3, 1, 6], [3, 4, 2], [5, 7, 1], [4, 0, 9], [7, 5, 5], [7, 0, 2], [2, 2, 9], [2, 0, 10], [3, 5, 7], [0, 6, 8], [0, 5, 5], [3, 2, 5], [3, 7, 3], [3, 6, 5], [4, 5, 4]]
# for transaction in transactions:
# 	g.add_transaction(transaction)
#
# nets = []
# for v_id in g.vs:
# 	v = g.vs[v_id]
# 	nets.append(v.net)
# nets.sort()
# print nets
# # print g.non_zero_nets


nodes = [ ["a","b"],["b","c"] ]
rels = [2.0,3.0]
queries = [ ["a","c"],["b","a"],["a","e"],["a","a"],["x","x"] ]
g = Graph()
for i in range(len(nodes)):
	v1_id, v2_id = nodes[i]
	rel = rels[i]
	g.add_relationship(v1_id, v2_id, rel)
result = []
for q in queries:
	result.append(g.get_relationship(q[0], q[1]))
print result
