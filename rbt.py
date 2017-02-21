from collections import deque

class RBNode:
	def __init__(self, val, parent = None, c = False):
		self.val = val
		self.c = c
		self.parent = parent
		self.left = None
		self.right = None

class RBT:
	def __init__(self):
		self.root = None

	def __rotate_left__(self, root, change_c = False):
		if not root or not root.parent:
			raise Exception('Must supply a root and it must have a parent')
		if root.parent.right != root:
			raise Exception('Cannot rotate a left node left')
		if root.parent == self.root:
			self.root = root
		parent = root.parent
		parent.right = root.left
		if root.left:
			root.left.parent = parent
		if parent.parent:
			if parent.parent.left == parent:
				parent.parent.left = root
			else:
				parent.parent.right = root
		root.parent = parent.parent
		root.left = parent
		parent.parent = root
		if change_c:
			root.c = not root.c
			parent.c = not parent.c

	def __rotate_right__(self, root, change_c = False):
		if not root or not root.parent:
			raise Exception('Must supply a root and it must have a parent')
		if root.parent.left != root:
			raise Exception('Cannot rotate a right node right')
		if root.parent == self.root:
			self.root = root
		parent = root.parent
		parent.left = root.right
		if root.right:
			root.right.parent = parent
		if parent.parent:
			if parent.parent.right == parent:
				parent.parent.right = root
			else:
				parent.parent.left = root
		root.parent = parent.parent
		root.right = parent
		parent.parent = root
		if change_c:
			root.c = not root.c
			parent.c = not parent.c

	def show(self, root, width = 60):
		rows = deque([[root]])
		cs = {True: 'r', False: 'b'}
		while rows:
			cur_row = rows.popleft()
			next_row = []
			vals = []
			for node in cur_row:
				if node.left:
					next_row.append(node.left)
				if node.right:
					next_row.append(node.right)
				vals.append(str(node.val) + cs[node.c])
			print(' '.join(vals))
			if next_row:
				rows.append(next_row)

	def insert(self, val):
		if not self.root:
			self.root = RBNode(val)
			return val
		walker = self.root
		while (walker.val >= val and walker.left) or (walker.val < val and walker.right):
			if walker.val >= val:
				walker = walker.left
			else:
				walker = walker.right
		new_node = RBNode(val, walker, True)
		if walker.val >= val:
			walker.left = new_node
		else:
			walker.right = new_node
		self.__handle_rotations__(new_node)
		return new_node.val

	def __handle_rotations__(self, node):
		if not node.parent.c:
			return None
		else:
			if not node.parent.parent:
				raise Exception('Root is a red node but should be black')
			parent = node.parent
			uncle = self.__sibling__(parent)
			if uncle and uncle.c and parent.c:
				parent.c = False
				uncle.c = False
				if parent.parent != self.root:
					parent.parent.c = True
					self.__handle_rotations__(parent.parent)
					return None
				else:
					return None
			child_order = ''
			if parent.right == node:
				child_order += 'R'
			else:
				child_order += 'L'
			if parent.parent.right == parent:
				child_order += 'R'
			else:
				child_order += 'L'
			self.__perform_rotations__(node, parent, child_order)


	def __perform_rotations__(self, node, parent, child_order):
		if child_order == 'RR':
			self.__rotate_left__(node.parent, True)
		elif child_order == 'LL':
			self.__rotate_right__(node.parent, True)
		elif child_order == 'RL':
			self.__rotate_left__(node)
			self.__rotate_right__(node, True)
		else:
			self.__rotate_right__(node)
			self.__rotate_left__(node, True)


	def __sibling__(self, node):
		if not node or not node.parent:
			raise Exception('Node has no parent or does not exist')
		if node == node.parent.left:
			return node.parent.right
		else:
			return node.parent.left







# r = RBT()
# root = RBNode(20)
# root.left = RBNode(10)
# root.left.parent = root
# root.right = RBNode(30)
# root.right.parent = root
# right = root.right
# right.right = RBNode(40)
# right.right.parent = right
# right.right.left = RBNode(35)
# right.right.left.parent = right.right
# right.left = RBNode(25)
# right.left.parent = right
# r.__rotate_left__(right.left)
# r.show(root)

  #
  #    20
  # 10    30
  #     25  40
  #       35




r = RBT()
a = [10, 20, 30, 40, 50, 15, 18, 25, 33, 28]
for num in a:
	r.insert(num)
# r.insert(10)
# r.insert(20)
# r.insert(-10)
# r.insert(15)
# r.insert(17)
# r.insert(40)
# r.insert(50)
# r.insert(60)
r.show(r.root)
# print(r.root.right.left.left.val)
