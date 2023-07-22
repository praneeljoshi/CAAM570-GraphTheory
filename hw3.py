import networkx as nx
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain, combinations

def get_subtours(nodes, A):
    """
    function that retuns a list of subtours given a list of nodes
    """

    # genertating subset powerset of nodes
    subtours = list(chain.from_iterable(combinations(nodes, r) for r in range(3,len(nodes)-1)))

    return subtours

def find_ham_cycle(G):
    """
    Function that retunrs a hamtionian cycle in G
    """

    # Setting imporant variables
    A = np.matrix(nx.linalg.graphmatrix.adjacency_matrix(G).toarray())
    N = G.number_of_nodes()
    nodes = list(G.nodes())

    # gurobipy model
    m = gp.Model("find_ham_cycle")
    # adding varibles
    X = m.addVars(N,N, vtype=GRB.BINARY, name="x")
    #setting obejctive
    m.setObjective(gp.quicksum(X[i,j] for i in range(N) for j in range(N)), GRB.MINIMIZE)

    # add constriant to inusre this is a cycle
    m.addConstrs(gp.quicksum(X[i,j] for j in range(N)) == 2 for i in range(N))

    # contraint to insure matrix is symetric
    for i in range(N):
        m.addConstrs((X[i,j] == X[j,i] for j in range(N)))

    # subtour elimation contraint
    subtours = get_subtours(nodes,A)
    for subtour in subtours:
        subtour_len = len(subtour) -1
        m.addConstr((gp.quicksum(X[i,j] for i in subtour for j in subtour)) <= 2*subtour_len)

    # insuring we are just removing edges rather than creating new ones
    m.addConstrs(X[i,j]<=A[i,j] for i in range(N) for j in range(N))

    # optimize the model
    m.optimize()
    
    # checking if model is feasible
    try:
        x = m.getAttr('X', X.values())
    except:
        print("MODEL IS INFEASINBLE; no cycle exists")
        return nx.empty_graph()

    # returning new graph
    A_new = np.matrix(np.reshape(x,(N,N)))
    P = nx.convert_matrix.from_numpy_matrix(A_new)
    return P

def find_ham_path(G):
    """
    Function that retunrs a hamtionian path in G
    """
    
    # Setting imporant variables
    A = np.matrix(nx.linalg.graphmatrix.adjacency_matrix(G).toarray())
    N = G.number_of_nodes()
    nodes = list(G.nodes())

    # gurobipy model
    m = gp.Model("find_ham_cycle")
    # adding varibles
    X = m.addVars(N,N, vtype=GRB.BINARY, name="x")
    #setting obejctive
    m.setObjective(gp.quicksum(X[i,j] for i in range(N) for j in range(N)), GRB.MINIMIZE)

    # add assignment constraints to insure it is a path graph
    m.addConstr(gp.quicksum(X[i,j] for j in range(N) for i in range(N)) == 2*N-2)
    m.addConstrs(gp.quicksum(X[i,j] for j in range(N)) <= 2 for i in range(N))
    m.addConstrs(gp.quicksum(X[i,j] for j in range(N)) >= 1 for i in range(N))

    # subtour elimantion constraint
    subtours = get_subtours(nodes,A)
    #subtours.append((6,9,7,5,8))
    for subtour in subtours:
        subtour_len = len(subtour)-1
        m.addConstr((gp.quicksum(X[i,j] for i in subtour for j in subtour)) <= 2*subtour_len)

    # insuring the adjacny matrix is symteric
    for i in range(N):
        m.addConstrs((X[i,j] == X[j,i] for j in range(N)))

    # contraint to limit options to be related to orginal adjancny matrix
    m.addConstrs(X[i,j]<=A[i,j] for i in range(N) for j in range(N))

    # optimize the model
    m.optimize()

    # checking if model is feasible
    try:
        x = m.getAttr('X', X.values())
    except:
        print("MODEL IS INFEASINBLE; no path exists")
        return nx.empty_graph()
        
    # returning new graph
    A_new = np.matrix(np.reshape(x,(N,N)))
    P = nx.convert_matrix.from_numpy_matrix(A_new)
    return P



# testing functions with custom graph
G = nx.Graph()
vertex_set = [0, 1, 2, 3,4,5]
edge_set = [(0,1), (0,2), (0,3), (0,4),(0,5),(1,2),(1,3),(2,4),(3,5),(4,5)]

G.add_nodes_from(vertex_set)
G.add_edges_from(edge_set)
G = nx.complete_graph(5)
L = nx.line_graph(G)


#P = find_ham_path(G)
#C = find_ham_cycle(G)
C = nx.complement(L)
plt.figure(1)
ax = plt.subplot(131)
nx.draw(G,  with_labels = True)
ax.set_title("Orginal Graph")
ax = plt.subplot(132)
nx.draw(L,  with_labels = True)
ax.set_title("Hamltonian Path")
ax = plt.subplot(133)
nx.draw(C,  with_labels = True)
ax.set_title("Hamltonian Cycle")

# testing functions with Peterson graph
G = nx.petersen_graph()
P = find_ham_path(G)
C = find_ham_cycle(G)
plt.figure(2)
ax = plt.subplot(131)
nx.draw(G,  with_labels = True)
ax.set_title("Orginal Graph")
ax = plt.subplot(132)
nx.draw(P,  with_labels = True)
ax.set_title("Hamltonian Path")
ax = plt.subplot(133)
nx.draw(C,  with_labels = True)
ax.set_title("Hamltonian Cycle")

plt.show()  
