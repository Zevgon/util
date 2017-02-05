class SLLNode:
	def __init__(self, val):
		self.val = val
		self.next = None

class SLL:
	def __init__(self):
		self.head = SLLNode(None)
		self.tail = self.head

	def __iter__(self):
		self.current = self.head
		return self

	def __remove_node__(self, parent):
		if not parent.next:
			raise Exception('Node does not exist')
		parent.next = parent.next.next

	def append(self, val):
		if self.head.val == None:
			self.head.val = val
		else:
			new_node = SLLNode(val)
			self.tail.next = new_node
			self.tail = new_node

	def append_node(self, node):
		if not node or not node.val:
			raise Exception('Node must exist and must have a value')
		if self.head.val == None:
			self.tail = self.head
		else:
			self.tail.next = node
			self.tail = node

	def arrayify(self):
		result = []
		for node in self:
			result.append(node.val)
		return result

	def delete(self, val):
		if self.empty():
			raise Exception('List is empty, cannot delete')
		if self.head.val == val:
			self.head.val = None
			if self.head.next:
				self.head = self.head.next
		else:
			walker = self.head
			while walker.next:
				if walker.next.val == val:
					self.__remove_node__(walker)
					return val
				walker = walker.next
		return None

	def empty(self):
		return self.head.val == None

	def next(self):
		if self.current == None or self.current.val == None:
			self.current = self.head
			raise StopIteration
		else:
			cur_node = self.current
			self.current = self.current.next
			return cur_node

	def reverse(self):
		prev = None
		cur = self.head
		nex = self.head.next
		while cur:
			cur.next = prev
			prev = cur
			cur = nex
			if cur:
				nex = cur.next
		self.tail = self.head
		self.head = prev

	def reverse_rec(self, cur = None):
		if not cur:
			cur = self.head
			self.tail = self.head
		if not cur.next:
			self.tail.next = None
			self.head = cur
			return cur
		nex = self.reverse_rec(cur.next)
		nex.next = cur
		return cur

s = SLL()
# s.append(1)
for i in range(5):
	s.append(i)
#
# s.reverse_rec()
s.reverse_rec()
# s.reverse()
print s.arrayify()
