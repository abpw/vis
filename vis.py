import time
import pygraphviz as pgv
from PIL import Image
import os

# wrapper object for pgv.AGraph
class Graph(object):
	# E is a list of lists representing the adjacency matrix of the graph
	def __init__(self, E):
		# if set to True, images will automatically be displayed
		self.autovis = False

		# counts the number of images created
		self.imgCount = 0

		assert len(E) and len(E[0]) == len(E), "Adjacency matrix must be square and non-empty"

		# If the adjacency matrix is symmetric, the graph is undirected
		self.directed = False
		for i in xrange(len(E)):
			if not E[i][i]:
				self.directed = True
				break
			for j in xrange(i):
				if E[i][j] != E[j][i]:
					self.directed = True
					break

		# Create the AGraph
		self.G = pgv.AGraph(strict=True, directed=self.directed)
		self.G.node_attr['shape'] = 'ellipse'
		self.G.node_attr['style'] = 'filled'

		# Edges indexed by head then tail
		self.E = {}
		for i in xrange(len(E)):
			self.E[i] = {}

		# nodes in numerical order
		self.V = []

		def addEdge(i, j, weight):
			self.G.add_edge(i, j)
			self.E[i][j] = Edge(i, j, self, weight=weight)

		def addNode(i):
			self.G.add_node(i)
			self.V.append(Node(i, self))

		# Add edges
		for i in xrange(len(E)):
			addNode(i)
			for j in xrange(i):
				if E[i][j]:
					# In the adjacency matrix of a directed graph, the first coordinate
					# is the source and the second is the destination
					addEdge(i, j, weight=E[j][i])
				if self.directed and E[j][i]:
					addEdge(j, i, weight=E[i][j])

		self.size = len(E)

	def getNode(self, i):
		return self.V[i]

	def getEdge(self, i, j):
		try:
			return self.E[i][j]
		except KeyError:
			return None

	# generator that yeilds each node u for which u.color == color (default any color),
	# and condition(u) == True
	def getNodes(self, color=None, condition=lambda x: True):
		for u in self.V:
			if (not color or u.color == color) and condition(u):
				yield u

	# generator that yeilds each edge e for which e.color == color (default any color),
	# e.weight == weight if weight is numeric or weight(e.weight) == True otherwise,
	# and condition(e) == True
	# returns in sort order (default is arbitrary order)
	def getEdges(self, color=None, weight=None, condition=lambda x: True, sort=None):
		for e in sorted([edge for dest in self.E.values() for edge in dest.values()], cmp=sort):
			if (not color or u.color == color) and condition(u):
				if isinstance(weight, (int, float, long)) and e.weight == weight:
					yield e
				elif hasattr(weight, '__call__') and weight(e.weight):
					yield e

	# write the current graph to a file
	# if self.autovis is set to True, display the image and sleep for 'delay' seconds
	def show(self, delay=1):
		filename = 'graphs/image' + '{0:0>3d}'.format(self.imgCount) + '.png'
		if not os.path.exists('graphs'):
			os.makedirs('graphs')
		self.G.draw(filename, prog='dot')
		self.imgCount += 1
		if self.imgCount == 101:
			print 'Warning: over 100 images have been saved to disk. Consider killing the process.'
		if self.autovis:
			Image.open(filename).show()
			time.sleep(delay)

# Superclass for Node and Edge. Not too useful at the moment, but extensible
class Element(object):
	def setColor(self, color):
		self.pvgElement().attr['color'] = color

	def color(self):
		return self.getColor()

	def getColor(self):
		return self.pvgElement().attr['color']

# Node object
class Node(Element):
	# i is the intiger label for this node
	# g is the graph this node is part of
	def __init__(self, label, G):
		self.label = label
		self.G = G

		# These should be the same in an undirected graph
		self.edgesFrom = []
		self.edgesTo = []

		self.neighbors = []

		# Empty in an undirected graph
		self.backNeighbors = []

		self.setColor('gray')

	# return the pvg version of this node
	def pvgElement(self):
		return self.G.G.get_node(self.label)

	def __cmp__(self, other):
		if isinstance(other, (int, long)):
			return self.label - other
		else:
			return self.label - other.label

# Edge object
class Edge(Element):
	# head and tail are the end nodes of the edge, either numbers of Node objects
	# head points to tail along this edge in a directed graph: (head) ----> (tail)
	# head and tail are arbitrary in an undirected graph: (head) ----- (tail)
	# G is the graph this edge is a part of
	def __init__(self, head, tail, G, weight=1):
		self.G = G
		if isinstance(head, (int, long)):
			self.head = self.G.getNode(head)
		else:
			self.head = head
		if isinstance(tail, (int, long)):
			self.tail = self.G.getNode(tail)
		else:
			self.tail = tail

		self.head.edgesFrom.append(self)
		self.head.neighbors.append(self.tail)
		self.tail.edgesTo.append(self)
		if self.G.directed:
			self.head.edgesTo.append(self)
			self.tail.backNeighbors.append(self.head)
		else:
			self.tail.edgesFrom.append(self)
			self.tail.neighbors.append(self.head)

		self.setColor('black')
		self.setWeight(weight)

	def setWeight(self, weight):
		self.pvgElement().attr['weight'] = weight

	def weight(self):
		return self.getWeight()

	def getWeight(self):
		return self.pvgElement().attr['weight']

	# return the pvg version of this edge
	def pvgElement(self):
		return self.G.G.get_edge(self.head.label, self.tail.label)

	# takes one end and returns the other
	# if a non-adjacent node is given, returns None
	def follow(self, i):
		if i == self.head:
			return self.tail
		if i == self.tail:
			return self.head
		return None