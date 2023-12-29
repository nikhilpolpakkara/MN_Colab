import streamlit as st
import networkx as nx
from pyvis.network import Network

# Create a directed graph
net = Network()

# Define nodes and edges for the process flow
nodes = ['Start', 'Step 1', 'Step 2', 'End']
edges = [('Start', 'Step 1'), ('Step 1', 'Step 2'), ('Step 2', 'End')]

net.add_node(1, label="MODEL")
net.add_node(2, label="DUARBILITY")
net.add_node(3, label="CAL")
net.add_node(4, label="NVH")
net.add_node(5, label="VEHICLE 1")
net.add_node(6, label="VEHICLE 2")
net.add_node(7, label="VEHICLE 3")
net.add_edge(1, 2)
net.add_edge(1, 3)
net.add_edge(1, 4)
net.add_edge(2, 5)
net.add_edge(2, 6)
net.add_edge(2, 7)
# net.use_DOT = True
net.neighborhood_highlight = True
net.template = net.templateEnv.get_template(net.path)
net.show("mohit.html", notebook=False)

