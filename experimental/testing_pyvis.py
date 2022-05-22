# %% Setup for the network plot
from pyvis.network import Network

# %%
net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
#net.force_atlas_2based()

# for row in df_edges_joined.iterrows():
#     src = str(row[1]["source"])
#     dst = str(row[1]["target"])
#     wgt = row[1]["weight"]
net.add_node(n_id="A", title="A", mass=10)
net.add_node(n_id="B", title="B", mass=10)
net.add_node(n_id="C", title="C", mass=10)
net.add_node(n_id="D", title="D", mass=-10)
#net.add_edge("A", "A", value=0, hidden=True)
net.add_edge("A", "B", value=1)
net.add_edge("B", "C", value=1)
net.add_edge("C", "D", value=1)
net.add_edge("D", "A", value=100)
net.add_edge("C", "A", value=1)
net.show_buttons(filter_=['physics'])

#net.repulsion(node_distance=100, central_gravity=0.1, spring_length=100,\
#     spring_strength=0.1, damping=0.2)

net.show("example_simple.html")

# %%
neighbor_map = net.get_adj_list()
for node in net.nodes:
    node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])


# %%
import matplotlib.pyplot as plt
import networkx as nx

G = nx.cubical_graph()
subax1 = plt.subplot(121)
nx.draw(G)   # default spring_layout
subax2 = plt.subplot(122)
nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')



# %%
