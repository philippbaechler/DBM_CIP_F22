# %%
from matplotlib.pyplot import title
import pandas as pd
import numpy as np


# %% Load the authors and article_author table
# The article_author holds the information which author worked on which article.
# The authors table holds the author names
df_article_author = pd.read_csv("data/output/normalized/article_author.csv", index_col=0)
df_authors = pd.read_csv("data/output/normalized/authors.csv", index_col=0)


# %%
def increment_edges(a, b):
    if f"{a} - {b}" not in author_edges:
        author_edges[f"{a} - {b}"] = 1
    else:
        author_edges[f"{a} - {b}"] += 1


# %%
# For counting how many times each author worked with each other we create 
# a dictionary like this: {'0 - 1': 1, '2 - 3': 2, '4 - 5': 2, ...}
# We loop over each article, get the list of authors, and loop twice (nested)
# over this list. To make sure that we do not get double entries, we save the
# entries where the first index is smaller than the second.
# Example double entry: {'0 - 1': 1, '1 - 0': 1}

author_edges = {}
for idx in df_article_author["article_id"].unique():
    if idx >= 200:
        break
    df_idx_aa = df_article_author.loc[df_article_author["article_id"] == idx]
    sorted_author_list = sorted(list(dict.fromkeys(df_idx_aa["author_id"])))

    for a in sorted_author_list:
        for b in sorted_author_list:
            if a < b:
                increment_edges(a, b)
author_edges

# %%
# The previously prepared dictionary is now converted to an data frame. For this
# we split the key into source and target index. The data frame looks like this:
#  
# 	source	target	weight
# 0	     0	     1	     1
# 1	     2	     3       2
# ...

author_edges_cleaned = []
for key, value in author_edges.items():
    a,b = key.split(" - ")
    author_edges_cleaned.append([int(a), int(b), value])
    
df_edges = pd.DataFrame(author_edges_cleaned)
df_edges = df_edges.rename(columns={0:"source", 1:"target", 2:"weight"})
df_edges


# %%
# Here we exchange the author id's with their names. This will allow us to display
# their names later in the network plot.

df_edges_joined = df_edges.join(df_authors, on="source")
df_edges_joined = df_edges_joined.drop(["source", "id", "location"], axis=1)
df_edges_joined = df_edges_joined.rename(columns={"name": "source"})

df_edges_joined = df_edges_joined.join(df_authors, on="target")
df_edges_joined = df_edges_joined.drop(["target", "id", "location"], axis=1)
df_edges_joined = df_edges_joined.rename(columns={"name": "target"})

df_edges_joined.head()


# %% Setup for the network plot
from pyvis.network import Network
net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
net.force_atlas_2based()


# %%
for row in df_edges_joined.iterrows():
    src = str(row[1]["source"])
    dst = str(row[1]["target"])
    wgt = row[1]["weight"]
    net.add_node(n_id=src, title=src)
    net.add_node(n_id=dst, title=dst)
    net.add_edge(src, dst, value=float(wgt))


# %%
neighbor_map = net.get_adj_list()
for node in net.nodes:
    node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])


# %%
net.set_options("""
var options = {
  "nodes": {
    "color": {
      "highlight": {
        "border": "rgba(233,72,164,1)",
        "background": "rgba(249,167,255,1)"
      },
      "hover": {
        "border": "rgba(233,68,187,1)",
        "background": "rgba(251,174,255,1)"
      }
    }
  },
  "edges": {
    "color": {
      "highlight": "rgba(132,132,132,1)",
      "inherit": true,
      "opacity": 0.5
    },
    "smooth": false
  },
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -1658,
      "springLength": 375,
      "springConstant": 0.015,
      "damping": 0.7
    },
    "minVelocity": 0.75,
    "solver": "forceAtlas2Based"
  }
}
""")
#net.show_buttons(filter_=['physics'])
net.show("data/example.html")


# %%
