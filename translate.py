# -*- coding: utf-8 -*-
import string
import random
class Node:
	def __init__(self, key, value):
		self.key = key.lower()
		self.value = value
		self.left = None
		self.right = None
		self.heightLeft = 0
		self.heightRight = 0
		self.balance = lambda: self.heightLeft-self.heightRight
		self.parent = None	#For printing only

class Tree:
	def __init__(self):
		self.root = None
		self.newestNode = None	#For printing last inserted in another color

	def insert(self, key, value):
		tmpNode = Node(key,value)
		if self.root:
			self.root = self._insert(self.root, tmpNode)
		else:
			self.root = tmpNode
		self.newestNode = tmpNode

	def _insert(self, parent, node):
#		print 'started insert. parent:',parent.key,'node:',node.key
		if node.key == parent.key:	#Already exists, overwrite the old nodes value with the new and return
			parent.value = node.value
			return parent
		if node.key < parent.key:
			if parent.left == None:
				parent.left = node
				node.parent = parent
				parent.heightLeft = 1
#				print 'node',node.key,'inserted in left'
			else:
				parent.left = self._insert(parent.left, node)
			parent.heightLeft = max(parent.left.heightLeft,parent.left.heightRight) + 1
#			print 'left height of',parent.key,'is',parent.heightLeft
		else:
			if parent.right == None:
				parent.right = node
				node.parent = parent
				parent.heightRight = 1
#				print 'node',node.key,'inserted in right'
			else:
				parent.right = self._insert(parent.right, node)
			parent.heightRight = max(parent.right.heightLeft,parent.right.heightRight) + 1
#			print 'right height of',parent.key,'is',parent.heightRight
#		print 'balance of',parent.key,'is',parent.balance()
		if parent.balance() > 1:
			print '##### Rotating right#####'
			if parent.left.key <= node.key:
				print 'Double rotate right'
				parent.left = self.rotateLeft(parent.left)
			parent = self.rotateRight(parent)
		elif parent.balance() < -1:
			print '##### Rotating left #####'
			if parent.right.key > node.key:
				print 'Double rotate left'
				parent.right = self.rotateRight(parent.right)
			parent = self.rotateLeft(parent)
		return parent

	def search(self, key):
		node = self.root
		print 'Balance\tKey\tLeft h\tRight h'
		while node != None:
			print node.balance(),'\t', node.key,'\t', node.heightLeft,'\t', node.heightRight
			if node.key == key.lower():
				return node.value
			if key < node.key.lower():
				node = node.left
			else:
				node = node.right
		return None

	def translate(self, key):
		translation = self.search(key)
		print ('Translation: '+str(translation),"No translation found")[translation==None]

	def rotateRight(self, node):
		tmp = node.left
		node.left = tmp.right
		if node.left:
			node.heightLeft = max(node.left.heightLeft,node.left.heightRight) + 1
		else:
			node.heightLeft = 0
		tmp.right = node
		node = tmp
		node.heightRight = max(node.right.heightLeft,node.right.heightRight) + 1
		return node

	def rotateLeft(self, node):
		tmp = node.right
		node.right = tmp.left
		if node.right:
			node.heightRight = max(node.right.heightLeft,node.right.heightRight) + 1
		else:
			node.heightRight = 0
		tmp.left = node
		node = tmp
		node.heightLeft = max(node.left.heightLeft,node.left.heightRight) + 1
		return node

	#For printing tree
	#Code taken from http://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/bst.py
	def __str__(self):
		if self.root is None: return '<empty tree>'
		def recurse(node):
			if node is None: return [], 0, 0
			label = str(node.key)
			if node == self.newestNode:
				nodeColor = '\033[31m'
			else:
				nodeColor = '\033[37m'
			left_lines, left_pos, left_width = recurse(node.left)
			right_lines, right_pos, right_width = recurse(node.right)
			middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
			pos = left_pos + middle // 2
			width = left_pos + middle + right_width - right_pos
			while len(left_lines) < len(right_lines):
				left_lines.append(' ' * left_width)
			while len(right_lines) < len(left_lines):
				right_lines.append(' ' * right_width)
			if (middle - len(label)) % 2 == 1 and node.parent is not None and \
			   node is node.parent.left and len(label) < middle:
				label += '.'
			label = label.center(middle, '.')
			if label[0] == '.': label = ' ' + label[1:]
			if label[-1] == '.': label = label[:-1] + ' '
			lines = [' ' * left_pos + nodeColor + label + '\033[37m' + ' ' * (right_width - right_pos),
					 ' ' * left_pos + '/' + ' ' * (middle-2) +
					 '\\' + ' ' * (right_width - right_pos)] + \
			  [left_line + ' ' * (width - left_width - right_width) +
			   right_line
			   for left_line, right_line in zip(left_lines, right_lines)]
			return lines, pos, width
		return '\n'.join(recurse(self.root) [0])

t = Tree()
'''t.insert("hej","hi")
t.insert("nu","now")
t.insert("jag är en banan", "I am a banana")
t.insert("penis", "penis")
t.insert("asdf", "lkjh")'''
'''t.insert('xyz','a')
t.insert('xzy','b')
t.insert('yzx','e')
t.insert('yxz','f')
t.insert('zxy','d')
t.insert('zyx','c')'''
#t.insert('g','g')
'''t.insert('r','r')
t.insert('z','z')
t.insert('k','k')
t.insert('a','a')
t.insert('l','l')
t.insert('m','m')
t.insert('dd','dd')
t.insert('ba','ba')
t.insert('ab','ab')'''
#alph = list(string.ascii_lowercase)
#random.shuffle(alph)
alph = ['q', 'x', 'z', 'w', 'n', 'j', 'h', 'g', 'r', 'd', 'i', 'y', 'c', 'k', 'f', 'p', 'e', 'v', 'l', 's', 't', 'm', 'b', 'a', 'u', 'o']
for letter in alph:
	t.insert(letter, letter)
	print t
	print

while True:
	choice = raw_input('Options:\n\t1. Translate\n\t2. Insert\n\t3. Print tree\n\t4. Quit\nEnter option (number): ')
	if choice == '1':
		t.translate(raw_input('Word or sentence to translate: '))
	elif choice == '2':
		t.insert(raw_input('Lang 1: '),raw_input('Lang 2: '))
	elif choice == '3':
		print t
	elif choice == '4':
		break
