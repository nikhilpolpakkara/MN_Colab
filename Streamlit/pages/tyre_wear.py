import streamlit as st
from pymongo import MongoClient
import datetime
import Mongodb_querries
import sys

client = MongoClient("mongodb://localhost:27017/")
print(sys.getsizeof(client))
db = client["TNV"]
department_details_collection = db["department_details"]
test_activity_name = "tyre_wear"
department_name = "durability"
line_color = "#2a9df4"


def tyre_wear_entry():
    st.title(f":blue[{test_activity_name.upper()}]")

    tyre_wear_doc = Mongodb_querries.get_document_from_nested_array(
        collection=department_details_collection,
        collection_filter={'name': department_name},
        nested_array="test_activity",
        array_document_filter={"field_name": 'name', "field_value": test_activity_name}
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
                {
                    "variable_name": entry["name"],
                    "st_input_type": entry["st_input_type"],
                    "hide": entry["hide"],
                    "required": entry["required"],
                    "options": entry["options"] if "options" in entry else []
                }
            )

    for sub_class in expander_list.keys():
        for variable in expander_list[sub_class]["variables"]:
            label_extension = " *" if (variable["required"] == 1) else ""
            if not variable["hide"] == 1:
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
                # save_to_mongodb("tyre_wear", document_data)
