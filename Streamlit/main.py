import streamlit as st

from pymongo import MongoClient



def reset_page():
    for key in st.session_state.keys():
        st.session_state.key = ''
    # print(st.session_state.values)

def tyre_wear_page(department, test_activity,department_details):
    st.title(test_activity)
    # Add data entry fields for the specified department and test activity

    pipeline = [
        {"$match": {"name": department}},  # Match the document by its ID
        {"$project": {
            "test_activity": {
                "$filter": {
                    "input": "$test_activity",
                    "as": "activity",
                    "cond": {"$eq": ["$$activity.name", test_activity]}
                }
            },
            "_id": 0
        }}
    ]

    # Execute the aggregation pipeline
    result = list(department_details.aggregate(pipeline))[0]['test_activity'][0]


    input_data = [d for d in result['test_data']['itr']['basic_details']]+\
                 [d for d in result['test_data']['itr']['vehicle_details']]+ \
                 [d for d in result['test_data']['itr']['component_details']]+\
                 [d for d in result['test_data']['ptr']]
    # Example: Text input for data entry

    for entry in input_data:
        st.text_input(f"{entry}:",key=f"{test_activity}_{entry}", value="")



    # Add more data entry fields as needed

    # Example: Save button
    if st.button("Save"):
        st.success(f"Data saved for {department} - {test_activity}")

    # Add a reset button next to the Save button
    if st.button("Reset"):
        st.session_state.tyre_wear_remarks = ""
        # reset_page()

def emission_page(department, test_activity, department_details):
    print("inside_de")
    st.title(test_activity)
    # Add data entry fields for the specified department and test activity

    pipeline = [
        {"$match": {"name": department}},  # Match the document by its ID
        {"$project": {
            "test_activity": {
                "$filter": {
                    "input": "$test_activity",
                    "as": "activity",
                    "cond": {"$eq": ["$$activity.name", test_activity]}
                }
            },
            "_id": 0
        }}
    ]

    # Execute the aggregation pipeline
    result = list(department_details.aggregate(pipeline))[0]['test_activity'][0]

    input_data = [d for d in result['test_data']['itr']['basic_details']]+\
                 [d for d in result['test_data']['itr']['vehicle_details']]+ \
                 [d for d in result['test_data']['itr']['component_details']]+\
                 [d for d in result['test_data']['ptr']]

    # Example: Text input for data entry
    for entry in input_data:
        st.text_input(f"{entry}:",key=f"{test_activity}_{entry}", value="")

    if st.button("Save"):
        st.success(f"Data saved for {department} - {test_activity}")

    # Add a reset button
    if st.button("Reset"):
        reset_page()

# Main App
def main():
    # Connect to the local MongoDB server (you can replace this with your connection string)
    client = MongoClient("mongodb://localhost:27017/")

    # Access a specific database (it will be created if it doesn't exist)
    db = client["common"]
    department_details = db["department_details"]

    st.sidebar.title("Select Department and Test Activity")


    # Display a dropdown to select the department
    pipeline = [{"$project": {"_id": 0, 'dept_name': '$name'}}]
    result = list(department_details.aggregate(pipeline))
    dept_names = [doc["dept_name"] for doc in result]

    selected_department = st.sidebar.selectbox("Select Department", dept_names)


    # Display a dropdown to select the test activity within the selected department
    pipeline = [
        {"$match": {"name": selected_department}},
        {"$unwind": "$test_activity"},
        {"$project": {"test_activity.name": 1, "_id": 0}}
    ]
    activity_list = [doc['test_activity']['name'] for doc in list(department_details.aggregate(pipeline))]
    selected_test_activity = st.sidebar.selectbox("Select Test Activity", activity_list)


    # Display the data entry page based on the selected department and test activity
    if selected_test_activity == 'tyre_wear':
        tyre_wear_page(selected_department, selected_test_activity,department_details)
    elif selected_test_activity == 'emission':
        emission_page(selected_department, selected_test_activity,department_details)

if __name__ == "__main__":
    main()