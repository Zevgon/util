class Heap:
	def __init__(self, store = None, comparator = lambda x, y: x < y, prc = lambda x: x):
		if not store:
			store = []
		self.store = store
		self.comparator = comparator
		self.prc = prc
		if self.store:
			self.__heapify_store__()

	def __child_indices__(self, idx):
		children = [(idx + 1) * 2 - 1, (idx + 1) * 2]
		return children

	def delete(self, idx):
		if idx < 0 or idx >= len(self.store):
			raise Exception('Cannot delete item: index out of range')
		last = len(self.store) - 1
		self.__swap__(idx, last)
		ret_val = self.__pop__()
		self.__heapify_up__(idx)
		self.__heapify_down__(idx)
		return ret_val

	def empty(self):
		return not self.store

	def extract(self, num = 1):
		extracted_vals = []
		for x in range(0, num):
			if self.empty():
				return extracted_vals
			last_idx = len(self.store) - 1
			self.__swap__(0, last_idx)
			ret_val = self.__pop__()
			self.__heapify_down__()
			extracted_vals.append(ret_val)
		if len(extracted_vals) == 1:
			return extracted_vals[0]
		else:
			return extracted_vals

	def __get_child_swap__(self, idx):
		block = lambda child_idx: self.__should_swap__(idx, child_idx)
		options = filter(block, self.__child_indices__(idx))
		if len(options) == 0:
			return None
		elif len(options) == 1:
			return options[0]
		else:
			item1 = self.store[options[0]]
			item2 = self.store[options[1]]
			if self.comparator(self.prc(item1), self.prc(item2)):
				return options[0]
			else:
				return options[1]

	def __heapify_down__(self, idx = 0):
		swap_with = self.__get_child_swap__(idx)
		while swap_with:
			self.__swap__(idx, swap_with)
			idx = swap_with
			swap_with = self.__get_child_swap__(idx)

	def __heapify_store__(self):
		new_store = list(self.store)
		self.store = []
		for item in new_store:
			self.insert(item)

	def __heapify_up__(self, idx = None):
		if not idx:
			idx = len(self.store) - 1
		parent_idx = self.__parent_idx__(idx)
		while self.__should_swap__(parent_idx, idx):
			self.__swap__(parent_idx, idx)
			idx = parent_idx
			parent_idx = self.__parent_idx__(idx)

	def insert(self, *items):
		for item in items:
			self.store.append(item)
			self.__heapify_up__()

	ins = insert

	def length(self):
		return len(self.store)

	def __parent_idx__(self, idx):
		if idx % 2 == 0:
			return idx / 2 - 1
		else:
			return idx / 2

	def peek(self):
		if self.empty():
			return None
		else:
			return self.store[0]

	def __pop__(self):
		return self.store.pop()

	def __should_swap__(self, parent_idx, idx):
		if idx >= len(self.store) or parent_idx < 0:
			return False
		parent = self.store[parent_idx]
		child = self.store[idx]
		return not self.comparator(self.prc(parent), self.prc(child))

	def show(self):
		return self.store

	def sort(self):
		old_store = list(self.store)
		result = []
		while not self.empty():
			result.append(self.extract())
		self.store = old_store
		return result

	def __swap__(self, parent_idx, idx):
		self.store[parent_idx], self.store[idx] = self.store[idx], self.store[parent_idx]

# h = Heap()
# h.insert(4, 1, 6, 2, 4, 7, 2, 3, 4, 7, 2, 3)
# print h.show()
# print h.delete(4)
