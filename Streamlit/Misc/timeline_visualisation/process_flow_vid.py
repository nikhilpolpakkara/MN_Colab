import streamlit as st
from graphviz import Digraph


def visualize_process_flow():
    # Create a Digraph object
    dot = Digraph(comment='Process Flow')

    # Define nodes and edges for the process flow
    dot.node('A', 'Start')
    dot.node('B', 'Step 1')
    dot.node('C', 'Step 2')
    dot.node('D', 'End')

    dot.edges(['AB', 'BC', 'CD'])

    return dot


def main():
    st.title('Process Flow Visualization')

    # Visualize the process flow
    process_flow = visualize_process_flow()
    st.graphviz_chart(process_flow.source)


if __name__ == '__main__':
    main()
