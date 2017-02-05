from trie_node import TrieNode

class Trie:
	def __init__(self):
		self.root = TrieNode(None)

	def insert(self, string):
		self.validate(string)
		cur_node = self.root
		for char in string:
			if char in cur_node.children:
				cur_node = cur_node.children[char]
			else:
				new_node = TrieNode(char)
				cur_node.add_child(char, new_node)
				cur_node = new_node
		cur_node.set_end()

	def validate(self, string):
		if not string:
			raise Exception('Cannot add empty strings')

	def insert_and_find_suffixes(self, string):
		self.validate(string)
		cur_node = self.root
		ret_val = []
		count = 0
		for char in string:
			if cur_node.is_end:
				ret_val.append(count)
			if char in cur_node.children:
				cur_node = cur_node.children[char]
			else:
				new_node = TrieNode(char)
				cur_node.add_child(char, new_node)
				cur_node = new_node
			count += 1
		cur_node.set_end()
		return ret_val

	def include(self, string):
		cur_node = self.root
		for char in string:
			if char in cur_node.children:
				cur_node = cur_node.children[char]
			else:
				return False
		return cur_node.is_end

	def include_suffix_or_next_suffixes(self, i, string):
		cur_node = self.root
		found = True
		next_suffixes = []
		end_nodes = set()
		while i < len(string):
			if cur_node.is_end and cur_node not in end_nodes:
				next_suffixes.append(i)
				end_nodes.add(cur_node)
			if string[i] in cur_node.children and found:
				cur_node = cur_node.children[string[i]]
			else:
				found = False
			i += 1
		if found and cur_node.is_end:
			return True
		elif next_suffixes:
			return next_suffixes
		else:
			return False



class Solution(object):
	def findAllConcatenatedWordsInADict(self, words):
		t = Trie()
		result = []
		del(words[words.index('')])
		words.sort(key = lambda x: len(x))
		for idx, word in enumerate(words):
			if word == '':
				words[-1], words[idx] = words[idx], words[-1]
				words.pop()
				break
		for word in words:
			suffix_starts = t.insert_and_find_suffixes(word)
			seen_is = set(suffix_starts)
			for i in suffix_starts:
				check = t.include_suffix_or_next_suffixes(i, word)
				if check == True:
					result.append(word)
					break
				elif check == False:
					continue
				else:
					for i in check:
						if not i in seen_is:
							suffix_starts.append(i)
							seen_is.add(i)
		return result

f = open('./dictionary2.txt')
words = f.readlines()
words = list(map(lambda x: x.rstrip(), words))
# print words[0:150]
s = Solution()
print len(s.findAllConcatenatedWordsInADict(words))
