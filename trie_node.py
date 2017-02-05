class TrieNode:
	def __init__(self, val, is_end = False):
		self.val = val
		self.children = {}
		self.is_end = is_end

	def add_child(self, char, child):
		self.children[char] = child

	def set_end(self):
		self.is_end = True
