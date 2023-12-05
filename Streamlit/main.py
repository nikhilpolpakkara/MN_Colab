import streamlit as st
from pymongo import MongoClient
<<<<<<< Updated upstream

import Mongodb_querries
=======
from pages import tyre_wear
import datetime
import Mongodb_querries
import sys
from st_pages import Page, show_pages, hide_pages

>>>>>>> Stashed changes

client = MongoClient("mongodb://localhost:27017/")
db = client["TNV"]
<<<<<<< Updated upstream


def tyre_wear_page(department, test_activity, department_details):
    # print(test_activity)
    # st.title(test_activity)
=======
line_color = "#2a9df4"

# hide_pages(
#     [
#         Page("pages/tyre_wear.py", name="tyre_wear"),
#         Page("pages/DataEntry.py", "DATA ENTRY"),
#         Page("pages/Analytics.py", "DATA ANALYTICS"),
#      ]
# )


def tyre_collection():
    st.title(f":blue[Tyre Collection]")


def tyre_wear_page(department_name, test_activity_name, department_details_collection):

    """
    :param department_name: This is the name of the department to fetch the details for building UI
    :param test_activity_name: Name of the test activity for which page is created
    :param department_details_collection: The collection inside which the details are stored.
    :return: Nothing is returned, it just renders the page.
    """

    st.title(f":blue[{test_activity_name.upper()}]")
>>>>>>> Stashed changes

    tyre_wear_doc = Mongodb_querries.get_document_from_nested_array(
        collection=department_details_collection,
        collection_filter={'name': department_name},
        nested_array="test_activity",
        array_document_filter={"field_name": 'name', "field_value": test_activity_name}
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
<<<<<<< Updated upstream
                {"variable_name": entry["name"], "st_input_type": entry["st_input_type"], "hide": entry["hide"],
                 "required": entry["required"]})
=======
                {
                    "variable_name": entry["name"],
                    "st_input_type": entry["st_input_type"],
                    "hide": entry["hide"],
                    "required": entry["required"],
                    "options": entry["options"] if "options" in entry else []
                }
            )
>>>>>>> Stashed changes

    for sub_class in expander_list.keys():
        for variable in expander_list[sub_class]["variables"]:
            label_extension = " *" if (variable["required"] == 1) else ""
            if not variable["hide"] == 1:
<<<<<<< Updated upstream
                if variable["st_input_type"] == "selectbox":
                    expander_list[sub_class]["expander"].selectbox(variable["variable_name"] + label_extension,
                                                                   options=["Front", "Rear"],
                                                                   key = variable["variable_name"])
                else:
                    expander_list[sub_class]["expander"].text_input(variable["variable_name"] + label_extension,
                                                                    key=variable["variable_name"])

    if st.button("Save Document"):
=======
                if variable['variable_name'] == "date":
                    expander_list[sub_class]["expander"].date_input(
                        "SELECT DATE", datetime.datetime.now().date(),
                        key="date")
                else:
                    if variable['st_input_type'] == 'selectbox':
                        expander_list[sub_class]["expander"].selectbox(
                            variable["variable_name"],
                            key=f"{test_activity_name}_{variable['variable_name']}",
                            options=variable["options"]
                        )
                    else:
                        expander_list[sub_class]["expander"].text_input(
                            (variable["variable_name"] + label_extension).upper(),
                            key=variable["variable_name"])

    expander_list["component_details"]["expander"].write("If you can't find your tyre in the drop down add a new tyre in the "
                                                         "databse by clicking on the ADD NEW TYRE button below")
    expander_list["component_details"]["expander"].link_button("ADD NEW TYRE", url="add_tyre_bt")

    st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

    with st.container():
        for variable_dict in tyre_wear_doc["test_data"]:
            if "dependant_variables" in variable_dict:
                for option in variable_dict["options"]:
                    with st.expander((option + " entry").upper()):
                        for entry in variable_dict["dependant_variables"]:
                            st.text_input(entry.upper(), key=f"{option}_{entry}")


    st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

    if st.button(("Save").upper(), use_container_width=True):
>>>>>>> Stashed changes
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
    result = db[collection_name].insert_one(document_data)
    # Check if the insertion was successful
    if result.inserted_id:
        st.success("Document saved to MongoDB successfully!")
    else:
        st.error("Error saving document to MongoDB.")


def data_entry_page():
    department_details = db["department_details"]

    st.sidebar.title("Select Department and Test Activity")

    dept_names = Mongodb_querries.get_field_values_from_collection(collection=department_details, field_name='name')

<<<<<<< Updated upstream
    selected_department = st.sidebar.selectbox("Select Department", dept_names)
=======
    with entry_expander:
        st.header(
            ":blue[SELECT DEPARTMENT & TEST ACTIVITY]"
        )
>>>>>>> Stashed changes

    activity_list = Mongodb_querries.get_field_values_from_nested_array(collection=department_details,
                                                                        collection_field_name='test_activity',
                                                                        array_field_name='name',
                                                                        filter={'name': selected_department})
    selected_test_activity = st.sidebar.selectbox("Select Test Activity", activity_list)

    # Display the data entry page based on the selected department and test activity
    # if selected_test_activity == 'tyre_wear':
    #     # tyre_wear_page(selected_department, selected_test_activity, department_details)
    #     tyre_wear.tyre_wear_entry()
    # elif selected_test_activity == 'emission':
    #     # emission_page(selected_department, selected_test_activity, department_details)
    #     tyre_collection()


def home_page():
    st.title = "HOME"
    col1, col2 = st.columns(2)
    with col1:
        st.button("ANALYTICS")

    with col2:
        st.button("DATA ENTRY", on_click=data_entry_page)


counter = 0


# Main App
def main():
    global counter
    counter += 1
    if counter == 1:
        home_page()
    print(counter)


if __name__ == "__main__":
    main()