import streamlit as st
from pymongo import MongoClient

import Mongodb_querries


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
                {"variable_name": entry["name"], "st_input_type": entry["st_input_type"], "hide": entry["hide"]})


    # print(expander_list)

    for sub_class in expander_list.keys():
        for variable in expander_list[sub_class]["variables"]:
            if not variable["hide"] == 1:
                if variable["st_input_type"] == "selectbox":
                    expander_list[sub_class]["expander"].selectbox(variable["variable_name"], options=["Front", "Rear"])
                else:
                    expander_list[sub_class]["expander"].text_input(variable["variable_name"])


def emission_page(department, test_activity, department_details):
    st.title(test_activity)


# Main App
def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["TNV"]
    department_details = db["department_details"]

    st.sidebar.title("Select Department and Test Activity")

    dept_names = Mongodb_querries.get_field_values_from_collection(collection= department_details, field_name='name')

    selected_department = st.sidebar.selectbox("Select Department", dept_names)

    activity_list = Mongodb_querries.get_field_values_from_nested_array(collection=department_details,
                                                                        collection_field_name='test_activity',
                                                                        array_field_name='name',
                                                                        filter={'name': selected_department})
    selected_test_activity = st.sidebar.selectbox("Select Test Activity", activity_list)

    # Display the data entry page based on the selected department and test activity
    if selected_test_activity == 'tyre_wear':
        tyre_wear_page(selected_department, selected_test_activity,department_details)
    elif selected_test_activity == 'emission':
        emission_page(selected_department, selected_test_activity,department_details)


if __name__ == "__main__":
    main()