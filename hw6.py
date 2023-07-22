import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def find_cut_vertex(G):

    list_cut = []
    num_comp = nx.number_connected_components(G)
    for node in G.nodes():
        G_copy = G.copy()
        G_copy.remove_node(node) 
        if nx.number_connected_components(G_copy)>num_comp:
            list_cut.append(node)
        

    return list_cut
        

# testing functions with custom graph
G = nx.Graph()
vertex_set = list(range(1,17))
edge_set = [(7,1), (1,16),(1,8),(2,6),(2,3),(2,10),(3,7),(3,6),(4,8),(4,5),(4,9),(5,11),(5,9),(6,10),(7,10),(8,11),(9,11),(12,15),(12,16),(12,14),(13,16),(13,15),(13,14),(14,15)]
G.add_nodes_from(vertex_set)
G.add_edges_from(edge_set)
list_cut = find_cut_vertex(G)
plt.figure(1)
ax = plt.subplot(121)
nx.draw(G,  with_labels = True)
ax.set_title("Orginal Graph")
ax = plt.subplot(122)
color_map = []
ax.set_title("Cut Vertex in red Graph")
for node in G.nodes():
    if node in list_cut:
        color_map.append('red')
    else:
        color_map.append('blue')
nx.draw(G, node_color=color_map, with_labels=True)

plt.show()
 