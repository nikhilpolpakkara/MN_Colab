import streamlit as st

# Define data for different departments and their test activities
departments = {
    "Department A": ["Test Activity 1A", "Test Activity 2A", "Test Activity 3A"],
    "Department B": ["Test Activity 1B", "Test Activity 2B", "Test Activity 3B"],
    # Add more departments and activities as needed
}


# Function to create the home page
def home_page():
    st.sidebar.title("Select Department")
    selected_department = st.sidebar.button("Home", key="home")

    for department in departments:
        if st.sidebar.button(department, key=department):
            return department

    return selected_department


# Function to create the department page
def department_page(department):
    st.sidebar.title(f"{department} Options")
    st.sidebar.button("Home", key="home")
    st.sidebar.write(f"Selected Department: {department}")

    selected_test_activity = st.sidebar.radio("Select Test Activity", departments[department])
    return selected_test_activity

# Main App
page = home_page()

if page == "home":
    st.title("Home Page")
else:
    st.title("Data Entry Page")
    selected_test_activity = department_page(page)
    st.write(f"Selected Test Activity: {selected_test_activity}")
    # Add data entry fields or other components for the selected test activity

