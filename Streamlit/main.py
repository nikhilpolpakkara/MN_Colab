import streamlit as st

from pymongo import MongoClient

# Connect to the local MongoDB server (you can replace this with your connection string)
client = MongoClient("mongodb://localhost:27017/")

# Access a specific database (it will be created if it doesn't exist)
db = client["common"]
department_details = db["department_details"]

pipeline = [ {"$project":{"_id": 0,'dept_name':'$name'}}]

result = list(department_details.aggregate(pipeline))

dept_names = [doc["dept_name"] for doc in result]



# Define functions for data entry on different pages
def data_entry_page(department, test_activity):
    st.title(selected_test_activity)
    # Add data entry fields for the specified department and test activity

    # Example: Text input for data entry
    for entry in department_details[department][test_activity]["entry_fields"]:
        data_entry_field = st.text_input(f"{entry}:")

    # Add more data entry fields as needed

    # Example: Save button
    if st.button("Save"):
        st.success(f"Data saved for {department} - {test_activity}: {data_entry_field}")

# Main App
st.sidebar.title("Select Department and Test Activity")

# Display a dropdown to select the department
selected_department = st.sidebar.selectbox("Select Department", dept_names)
pipeline = [
    {"$match": {"name": selected_department}},
    {"$unwind": "$test_activity"},
    {"$project": {"test_activity.name": 1, "_id": 0}}
]

activity_list = [doc['test_activity']['name'] for doc in list(department_details.aggregate(pipeline))]

# Display a dropdown to select the test activity within the selected department
selected_test_activity = st.sidebar.selectbox("Select Test Activity", activity_list)

# Display the data entry page based on the selected department and test activity
data_entry_page(selected_department, selected_test_activity)
