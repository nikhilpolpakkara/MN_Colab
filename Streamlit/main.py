import streamlit as st
from pymongo import MongoClient

import Mongodb_querries

client = MongoClient("mongodb://localhost:27017/")
db = client["TNV"]


def tyre_wear_page(department, test_activity, department_details):
    st.title(test_activity)
    #
    # # Example: Save button
    # if st.button("Save"):
    #     st.success(f"Data saved for {department} - {test_activity}")
    tyre_wear_doc = Mongodb_querries.get_document_from_nested_array(
        collection=department_details,
        collection_filter={'name': department},
        nested_array="test_activity",
        array_document_filter={"field_name": 'name', "field_value": test_activity}
        )

    expander_list = {}

    for entry in tyre_wear_doc["test_data"]:
        if entry["class"] in ["itr", "td"]:
            sub_class = entry["sub_class"]
            if sub_class not in expander_list.keys():
                expander_list[sub_class] = {
                    "expander": st.expander(sub_class),
                    "variables": []
                }

            expander_list[sub_class]["variables"].append(
                {"variable_name": entry["name"], "st_input_type": entry["st_input_type"], "hide": entry["hide"],
                 "required": entry["required"]})

    # print(expander_list)

    for sub_class in expander_list.keys():
        for variable in expander_list[sub_class]["variables"]:
            label_extension = " *" if (variable["required"] == 1) else ""
            if not variable["hide"] == 1:
                if variable["st_input_type"] == "selectbox":
                    expander_list[sub_class]["expander"].selectbox(variable["variable_name"] + label_extension,
                                                                   options=["Front", "Rear"],
                                                                   key = variable["variable_name"])
                else:
                    expander_list[sub_class]["expander"].text_input(variable["variable_name"] + label_extension,
                                                                    key=variable["variable_name"])

    if st.button("Save Document"):
        for entry in tyre_wear_doc["test_data"]:
            if (entry['required'] == 1) & (st.session_state[entry['name']] == ""):
                save_to_db = False
                st.error(f"Please enter {entry['name']} field")
                break
            else:
                save_to_db = True
        if save_to_db:
            save_to_mongodb("tyre_wear", st.session_state)


def emission_page(department, test_activity, department_details):
    st.title(test_activity)


def save_to_mongodb(collection_name, document_data):
    # Insert the document into the MongoDB collection
    collection = db[collection_name]
    result = collection.insert_one(document_data)
    # Check if the insertion was successful
    if result.inserted_id:
        st.success("Document saved to MongoDB successfully!")
    else:
        st.error("Error saving document to MongoDB.")


# Main App
def main():
    department_details = db["department_details"]

    st.sidebar.title("TNV APP")

    analytics_expander = st.sidebar.expander("ANALYTICS", expanded=True)
    entry_expander = st.sidebar.expander("DATA ENTRY", expanded=True)

    with analytics_expander:
        st.write("Analytics")

    with entry_expander:

        dept_names = Mongodb_querries.get_field_values_from_collection(collection=department_details,
                                                                       field_name='name')

        selected_department = st.selectbox("Select Department", dept_names)

        activity_list = Mongodb_querries.get_field_values_from_nested_array(collection=department_details,
                                                                            collection_field_name='test_activity',
                                                                            array_field_name='name',
                                                                            filter={'name': selected_department})
        selected_test_activity = st.selectbox("Select Test Activity", activity_list)

    # Display the data entry page based on the selected department and test activity
    if selected_test_activity == 'tyre_wear':
        tyre_wear_page(selected_department, selected_test_activity, department_details)
    elif selected_test_activity == 'emission':
        emission_page(selected_department, selected_test_activity, department_details)


if __name__ == "__main__":
    main()