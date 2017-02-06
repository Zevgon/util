class BT:
	def __init__(self):
		self.store = []

	def __child_ids__(self, parent_id):
		return [parent_id * 2 + 1, parent_id * 2 + 2]

	def __parent_id__(self, child_id):
		return (child_id - 1) / 2

	def insert(self, val):
		self.store.append(val)

	def insert_left(self, parent_id, val):
		child_id = self.__child_ids__(parent_id)[0]
		if child_id < len(self.store) and self.store[child_id]:
			raise Exception('Left child already exists for parent_id {0}'.format(parent_id))
		elif len(self.store) <= child_id:
			while len(self.store) <= child_id:
				self.store.append(None)
		self.store[child_id] = val

	def insert_right(self, parent_id, val):
		child_id = self.__child_ids__(parent_id)[1]
		if x < len(self.store) and self.store[x]:
			raise Exception('Right child already exists for parent_id {0}'.format(parent_id))
		elif len(self.store) <= x:
			while len(self.store) <= x:
				self.store.append(None)
		self.store[x] = val

	def left(self, parent_id):
		child_id = self.__child_ids__(parent_id)[0]
		if child_id >= len(self.store):
			return None
		else:
			return self.store[child_id]

	def right(self, parent_id):
		child_id = self.__child_ids__(parent_id)[1]
		if child_id >= len(self.store):
			return None
		else:
			return self.store[child_id]

	def children(self, parent_id):
		child_ids = self.__child_ids__(parent_id)
		result = []
		if child_ids[0] >= len(self.store):
			return [None, None]
		elif child_ids[1] >= len(self.store):
			return [self.store[child_ids[0]], None]
		else:
			return [self.store[child_ids[0]], self.store[child_ids[1]]]


# b = BT()
# for i in range(20):
# 	b.insert(i)
# print b.store
# print b.left(2)
# print b.right(2)
# print b.children(2)
# print b.children(18)
# b.insert_left(15, 2)
# print b.store
# print b.children(15)
