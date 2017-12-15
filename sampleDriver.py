# Depth first search example demonstrating the vis library

from vis import *

#	  0  1  2  3
E = [[0, 1, 1, 0], #0
	 [0, 0, 0, 1], #1
	 [0, 0, 0, 1], #2
	 [0, 0, 0, 0]] #3

graph = Graph(E)
graph.show() # Display the graph

limbo = []

root = graph.getNode(0) #DFS root
root.setColor('red')
limbo.append(root)
graph.show() # Update the display
while limbo:
	curr = limbo.pop()
	curr.setColor('blue')
	for edge in curr.edgesFrom:
		if edge.tail.color() != 'gray':
			continue
		edge.tail.setColor('red')
		limbo.append(edge.tail)
	graph.show()
	curr.setColor('green')
graph.show()