import streamlit as st

# Define the sidebar levels and sub-levels
levels = ['Dashboard', 'Data Entry', 'Analytics', 'Documentation', 'Misc']
sub_levels = {
    'Dashboard': ['Overview', 'Charts'],
    'Data Entry': ['Form', 'Upload Data'],
    'Analytics': ['Statistics', 'Visualizations'],
    'Documentation': ['User Guide', 'API Documentation'],
    'Misc': ['Settings', 'About']
}

# Create the main Streamlit app
def main():
    st.title("Streamlit App with Sidebar Levels and Expander")

    # Sidebar level selection
    selected_level = st.sidebar.selectbox("Select Level", levels)

    # Expander for sub-levels
    with st.sidebar.expander(f"Sub-Levels for {selected_level}"):
        selected_sub_level = st.selectbox(f"Select Sub-Level for {selected_level}", sub_levels.get(selected_level, []))

    # Display content based on the selected level and sub-level
    st.write(f"You selected: {selected_level} > {selected_sub_level}")

# Run the app
if __name__ == "__main__":
    main()
