import streamlit as st
from pymongo import MongoClient

import datetime
import Mongodb_querries
import sys


client = MongoClient("mongodb://localhost:27017/")
print(sys.getsizeof(client))
db = client["TNV"]
line_color = "#2a9df4"


def tyre_wear_page(department, test_activity, department_details):

    st.title(f":blue[{test_activity.upper()}]")

    tyre_wear_doc = Mongodb_querries.get_document_from_nested_array(
        collection=department_details,
        collection_filter={'name': department},
        nested_array="test_activity",
        array_document_filter={"field_name": 'name', "field_value": test_activity}
        )

    expander_list = {}

    for entry in tyre_wear_doc["test_data"]:
        if entry["class"] in ["itr"]:
            sub_class = entry["sub_class"]
            if sub_class not in expander_list.keys():
                expander_list[sub_class] = {
                    "expander": st.expander(sub_class.upper()),
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
                if variable['variable_name'] == "date":
                    expander_list[sub_class]["expander"].date_input("SELECT DATE", datetime.datetime.now().date(), key="date")
                else:
                    expander_list[sub_class]["expander"].text_input((variable["variable_name"] + label_extension).upper(),
                                                                    key=variable["variable_name"])

    st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

    with st.container():
        for variable_dict in tyre_wear_doc["test_data"]:
            if "dependant_variables" in variable_dict:
                for option in variable_dict["options"]:
                    with st.expander((option + " entry").upper()):
                        for entry in variable_dict["dependant_variables"]:
                            st.text_input(entry.upper(), key=f"{option}_{entry}")

    # print(st.session_state)

    st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

    if st.button(("Save").upper(), use_container_width=True):
        for entry in tyre_wear_doc["test_data"]:
            try:
                if (entry['required'] == 1) & (st.session_state[entry['name']] == ""):
                    save_to_db = False
                    st.error(f"Please enter {entry['name']} field")
                    break
                else:
                    save_to_db = True
            except:
                pass
        if save_to_db:
            document_data = dict(st.session_state)
            document_data["date"] = document_data['date'].strftime('%d-%m-%Y')
            document_data["date_time"] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            save_to_mongodb("tyre_wear", document_data)


def emission_page(department, test_activity, department_details):
    st.title(test_activity.upper())


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

    st.sidebar.title(":blue[SELECT DEPARTMENT & TEST ACTIVITY]")

    st.sidebar.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

    dept_names = Mongodb_querries.get_field_values_from_collection(collection= department_details, field_name='name')

    selected_department = st.sidebar.selectbox(("Select Department").upper(), dept_names)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    activity_list = Mongodb_querries.get_field_values_from_nested_array(collection=department_details,
                                                                        collection_field_name='test_activity',
                                                                        array_field_name='name',
                                                                        filter={'name': selected_department})
    selected_test_activity = st.sidebar.selectbox(("Select Test Activity").upper(), activity_list)

    # Display the data entry page based on the selected department and test activity
    if selected_test_activity == 'tyre_wear':
        tyre_wear_page(selected_department, selected_test_activity,department_details)
    elif selected_test_activity == 'emission':
        emission_page(selected_department, selected_test_activity,department_details)

    # Trigger an action, e.g., button click, to save the document


if __name__ == "__main__":
    main()