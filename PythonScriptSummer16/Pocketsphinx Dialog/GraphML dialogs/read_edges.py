import networkx as nx
import argparse
import sys


G = nx.read_graphml("write_graphml.graphml", unicode)

root = 'n1'
current = root

for edge in G.edges(current, data = True):
	print str(edge[2].values()[0])
	current = edge[1]

"^(computer science)"
