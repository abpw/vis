from vis import *

#	  A  B  C  D
E = [[0, 1, 1, 0], #A
	 [0, 0, 0, 1], #B
	 [0, 0, 0, 1], #C
	 [0, 0, 0, 0]] #D

graph = Graph(E)
graph.show() # Display the graph

limbo = []

root = graph.getNode(0) #DFS root
root.color = 'red'
limbo.append(root)
graph.show() # Update the display
while limbo:
	curr = limbo.pop()
	curr.color = 'green'
	for edge in curr.edgesFrom:
		edge.tail.color = 'red'
		limbo.append(edge.tail)
	graph.show()