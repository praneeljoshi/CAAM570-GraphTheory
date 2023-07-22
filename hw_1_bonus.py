# importing networkx and pyplot
import networkx as nx
import matplotlib.pyplot as plt

#creating and plotting the peterson graph
peterson = nx.petersen_graph()
subax1 = plt.subplot(221)
subax1.title.set_text('Peterson Graph')
nx.draw(peterson, with_labels=True, font_weight='bold')

#creating and plotting the complment of the peterson graph
peterson_complemt = nx.complement(peterson)
subax2 = plt.subplot(222)
subax2.title.set_text('Complement of Peterson Graph')
nx.draw(peterson_complemt, with_labels=True, font_weight='bold')

#creating and plotting the line of the peterson graph
peterson_line = nx.line_graph(peterson)
subax3 = plt.subplot(223)
subax3.title.set_text('Line of Peterson Graph')
nx.draw(peterson_line, with_labels=True, font_weight='bold')

# showing plot
plt.show()  
