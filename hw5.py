import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def fleury(G):
    # setting important variables
    E = G.edges()
    V = G.nodes()
    odd_cnt = 0
    odd_node= 0
    G_temp = G.copy()
    path = []

    # looping through vertices and counting odd degree vertices
    for v in V:
        if G_temp.degree[v]%2!=0:
            odd_cnt+=1
            odd_node = v
    
    # if odd degree vertices are not zero or 2 graph or if graph is not connected
    #  then graph does not have euler path/circut
    if odd_cnt == 1 or odd_cnt>2 or not nx.is_connected(G_temp):
        print("Graph does not have am Euler Path/Circut")
        return 'No Euler Path/Circut exsits'

    # setting starting vertex depdning on odd vertex
    if odd_cnt == 0:
        current_node = list(G_temp.nodes())[0]
        print(current_node)
        print("Euler Cicuit found")
    else:
        current_node = odd_node
        print("Euler Path found")

    # setting starting node
    path.append(current_node)

    # looping until there are no edges left
    while 1:
        
        # case where current node does not have any neighbors
        if G_temp.degree[current_node] == 0:
            break

        # case where current node has one neighbor
        elif G_temp.degree[current_node] == 1:
            # setting next node and removing edge
            next_node = list(G_temp.neighbors(current_node))[0]  
            G_temp.remove_edge(current_node,next_node)
            current_node = next_node
            path.append(current_node)
        
        # case where current node has many neighbors
        else:

            # finding all neighbors of the current node and bridges of the current G
            neighbors = G_temp.neighbors(current_node)
            bridges = list(nx.bridges(G_temp, root=None))

            # chosing next node by insuring that it is not a bridge edge
            for n in neighbors:
                if not (current_node,n) in bridges or not (n,current_node) in bridges:
                    # setting next node and removing edge
                    G_temp.remove_edge(current_node,n)
                    current_node = n
                    path.append(current_node)
                    break
    
    # making string of path
    path_str = ''
    cnt = 1
    for v in path:
        if cnt != len(path):
            path_str += str(v)+ '-'
        else:
            path_str += str(v)
        cnt = cnt +1

    return path_str
        

# testing functions with custom graph
G = nx.Graph()
vertex_set = [0, 1, 2, 3]
edge_set = [(0,1), (1,3), (3,2), (2,1),(0,3)]
G.add_nodes_from(vertex_set)
G.add_edges_from(edge_set)
P = fleury(G)
plt.figure(1)
ax = plt.subplot(121)
nx.draw(G,  with_labels = True)
ax.set_title("Orginal Graph")
ax = plt.subplot(122)
ax.text(0.5, 0.5, P, size=24, ha='center', va='center')
ax.set_title("Euler Circuit/Path")

G = nx.Graph()
vertex_set = [0, 1, 2, 3]
edge_set = [(0,1), (1,2), (3,2), (3,0)]
G.add_nodes_from(vertex_set)
G.add_edges_from(edge_set)
P = fleury(G)
plt.figure(2)
ax = plt.subplot(121)
nx.draw(G,  with_labels = True)
ax.set_title("Orginal Graph")
ax = plt.subplot(122)
ax.text(0.5, 0.5, P, size=24, ha='center', va='center')
ax.set_title("Euler Circuit/Path")

# testing functions with Peterson graph
G = nx.petersen_graph()
P = fleury(G)
plt.figure(3)
ax = plt.subplot(121)
nx.draw(G,  with_labels = True)
ax.set_title("Orginal Graph")
ax = plt.subplot(122)
ax.text(0.5, 0.5, P, size=24, ha='center', va='center')
ax.set_title("Euler Circuit/Path")

plt.show()
 