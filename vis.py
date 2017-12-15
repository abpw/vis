import time
import pygraphviz as pgv

# wrapper object for pgv.AGraph
class Graph(object):
	# E is a list of lists representing the adjacency matrix of the graph
	def __init__(self, E):
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
		self.G = psv.AGraph(strict=True, directed=self.directed)

		def addEdge(i, j):
			# New method for edges: takes one end and returns the other
			# if a non-adjacent node is given, returns None
			def follow(self, i):
				if i == self.head:
					return self.tail
				if i == self.tail:
					return self.head
				return None

			self.G.add_edge(i, j)
			e = self.getEdge(i, j)
			e.weight = Weight(e)
			e.color = Color(e, color='black')
			e.head = self.getNode(i)
			e.tail = self.getNode(i)
			e.follow = follow.__get__(e)
			self.E.append(e)

		def addNode(i):
			# New method for 
			self.G.add_node(i)
			u = self.getNode(i)
			u.color = Color(u)
			u.edgesFrom = []
			u.edgesTo = []
			u.children = []
			u.parents = []


		self.E = []
		# Add edges
		for i in xrange(len(E)):
			addNode(i)
			for j in xrange(i):
				if E[i][j]:
					# In the adjacency matrix of a directed graph, the first coordinate
					# is the source and the second is the destination
					addEdge(i, j)
				if self.directed and E[j][i]:
					addEdge(j, i)

			top = len(E) if self.directed else i
			for j in xrange(top):
				if E[i][j]:
					v.addEdge(i+1, j+1, weight=E[i][j])

		self.size = len(E)

	def getNode(self, i):
		return self.G.get_node(i)

	def getEdge(self, i, j):
		return self.G.get_edge(i, j)

	# generator that yeilds each node u for which u.color == color (default any color),
	# and condition(u) == True
	def getNodes(self, color=None, condition=lambda x: True):
		for i in xrange(self.size):
			u = self.getNode(i)
			if (not color or u.color == color) and condition(u):
				yield u

	# generator that yeilds each edge e for which e.color == color (default any color),
	# e.weight == weight if weight is numeric or weight(e.weight) == True otherwise,
	# and condition(e) == True
	def getEdges(self, color=None, weight, condition=lambda x: True):
		for e in self.E:
			if (not color or u.color == color) and condition(u):
				if isinstance(weight, (int, float, long)) and e.weight == weight:
					yield e
				elif hasattr(weight, '__call__') and weight(e.weight):
					yield e

	def show(self, delay=1):
		pass
		time.sleep(delay)

# used for the descriptor protocol to add the '.color' shorthand to nodes and edges
class Color(object):
	def __init__(self, element, color='white'):
		self.element = element
		self.element.attr['color'] = color

	def __set__(self, color):
		self.element.attr['color'] = color

	def __get__(self):
		return self.element.attr['color']

# used for the descriptor protocol to add the '.weight' shorthand to edges
class Weight(object):
	def __init__(self, edge):
		self.edge = edge

	def __set__(self, color):
		self.edge.attr['color'] = color

	def __get__(self):
		return self.edge.attr['color']

'''
class Vertex(object):
	def __init__(self, label, graph, color='white'):
		self.label = label
		self.graph = graph
		self.color = color
		self.children = {}
		self.parents = {}

	def addEdge(self, child, weight=1, iterate=True):
		self.graph.add_edge(self.label, child.label, weight=weight)
		self.children[child] = weight
		child.parents[self] = weight
		if not self.graph.directed and iterate:
			child.addEdge(self, weight, False)


	def color(self, color):
		self.color = color
		self.graph.get_node(self.label).attr['color'] = color'''