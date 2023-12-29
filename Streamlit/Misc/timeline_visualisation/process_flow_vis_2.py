import streamlit as st
import networkx as nx
from pyvis.network import Network


def visualize_process_flow():
    # Create a directed graph
    net = Network()

    # Define nodes and edges for the process flow
    nodes = ['Start', 'Step 1', 'Step 2', 'End']
    edges = [('Start', 'Step 1'), ('Step 1', 'Step 2'), ('Step 2', 'End')]

    net.add_node(1, label="Node 1")
    net.add_node(2, label="Node 2")
    net.add_edge(1, 2)

    return net


def main():
    st.title('Interactive Process Flow Visualization')

    # Visualize the process flow
    process_flow = visualize_process_flow()
    # st.pyplot(process_flow)
    st.write(process_flow.generate_html())


if __name__ == '__main__':
    main()
