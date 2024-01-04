import streamlit as st
import datetime
from DBOps import MongoDBOps

line_color = "#2a9df4"


def test_data_entry(tyre_wear_doc, test_data_handler, client):

    def fetch_vehicle_details():
        print("Fetching Vehicle Details")
        vehicle_details = vehicle_details_handler.get_document_from_level_1_collection(
            document_filter={"rev_no": st.session_state["veh_id"]}
        )
        st.session_state["model"] = vehicle_details["model"]
        st.session_state["chassis_no"] = vehicle_details["chassis_no"]
        st.session_state["batch"] = vehicle_details["batch"]

    st.title(f":blue[{tyre_wear_doc['name'].upper()}]")

    tab1, tab2, tab3 = st.tabs(["Test Data Entry", "Add New Vehicle", "Add New tyre"])

    vehicle_details_handler = test_data_handler
    vehicle_details_handler.load_collection("vehicle_details")
    options_dict = {
       "veh_id": vehicle_details_handler.get_field_values_from_level_1_collection(
           field_names=["rev_no"],
           project_id=True
       ),
    }

    with tab1:
        rev_no = st.selectbox(
            "REV NO".upper(),
            key="veh_id",
            options=options_dict["veh_id"],
            index=None,
            on_change=fetch_vehicle_details
        )
        with st.form("my_form"):
            expander_info_dict = {}

            for test_parameter in tyre_wear_doc["test_data"]:
                if test_parameter["class"] in ["itr"]:
                    sub_class = test_parameter["sub_class"]
                    if sub_class not in expander_info_dict.keys():
                        expander_info_dict[sub_class] = {
                            "st.expander": st.expander(sub_class.upper()),
                            "expander_entries": {}
                        }

                    expander_info_dict[sub_class]["expander_entries"][test_parameter["name"]] = {
                        "name": test_parameter["name"],
                        "st_input_type": test_parameter["st_input_type"],
                        "hide": test_parameter["hide"],
                        "required": test_parameter["required"],
                        "options": options_dict[test_parameter["name"]] if test_parameter["name"] in options_dict else []
                    }

            for expander in expander_info_dict.values():
                for test_parameter in expander["expander_entries"].values():
                    entry_label_extension = " *" if (test_parameter["required"] == 1) else ""
                    if not test_parameter["hide"] == 1:
                        if test_parameter['name'] == "date":
                            expander["st.expander"].date_input(
                                "SELECT DATE",
                                datetime.datetime.now().date(),
                                key="date"
                            )
                        else:
                            if test_parameter["st_input_type"] == "text_input":
                                expander["st.expander"].text_input(
                                    (test_parameter["name"] + entry_label_extension).upper(),
                                    key=test_parameter["name"])
                            elif test_parameter["st_input_type"] == "selectbox":
                                if not test_parameter["name"] == "veh_id":
                                    expander["st.expander"].selectbox(
                                        (test_parameter["name"] + entry_label_extension).upper(),
                                        key=test_parameter["name"],
                                        options=test_parameter["options"],
                                        index=None,
                                    )

            st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

            with st.container():
                for test_parameter in tyre_wear_doc["test_data"]:
                    if "dependant_variables" in test_parameter:
                        for option in test_parameter["options"]:
                            with st.expander((option + " entry").upper()):
                                for entry in test_parameter["dependant_variables"]:
                                    st.text_input(entry.upper(), key=f"{option}_{entry}")

            st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

            submitted = st.form_submit_button("SAVE TEST DATA", use_container_width=True)
            if submitted:
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
                    if "FormSubmitter:my_form-SAVE TEST DATA" in document_data:
                        del document_data["FormSubmitter:my_form-SAVE TEST DATA"]
                    result = test_data_handler.add_document_to_collection(document_data)

                    if result == 1:
                        st.success("Document saved to MongoDB successfully!")
                    else:
                        st.error("Error saving document to MongoDB.")

    with tab2:
        new_model = st.selectbox("Is it a new model ?", options=["NO", "YES"])
        with st.form("vehicle_form"):
            if new_model == "NO":
                model = st.selectbox("Model", options=[])
            else:
                model = st.text_input("Model")

            rev_no = st.text_input("REV No")
            chasis_no = st.text_input("Chasis No")
            engine_no = st.text_input("Engine No")
            description = st.text_area("Additional Information")

            vehicle_form_submit = st.form_submit_button("Submit")

            if vehicle_form_submit:
                data_document = {
                    "rev_no": rev_no,
                    "model": model,
                    "chasis_no": chasis_no,
                    "engine_no": engine_no,
                    "description": description

                }

    with tab3:
        with st.form("tire_form"):
            wheel_position = st.selectbox("Wheel Postion", options=["front", "rear"], index=None)
            make = st.text_input("Tyre Make")
            section_width = st.number_input("Section Width", step=5)
            aspect_ration = st.number_input("Aspect Ratio", step=5)
            rim_dia = st.number_input("Rim Diameter", step=1)
            twi = st.text_input("TWI")
            load_index = st.text_input("Load Index")
            speed_rating = st.text_input("Speed Rating")
            tubing = st.selectbox("Tubing Type", ["Tubeless", "Tube"], index=None)
            tread_pattern = st.selectbox("Tread Pattern", ["all_weather", "summer", "winter"], index=None)
            tyre_form_submit = st.form_submit_button("Submit")

            if tyre_form_submit:
                db_handler = MongoDBOps.MongoDBHandler(client)
                db_handler.load_database("common")
                db_handler.load_collection("counter")
                tyre_id = db_handler.generate_id(counter="tyre_id")
                new_tyre_document = {
                    "tyre_id": tyre_id,
                    "wheel_position": wheel_position,
                    "make": make,
                    "section_width": section_width,
                    "aspect_ration": aspect_ration,
                    "rim_dia": rim_dia,
                    "size": f"{section_width}/{aspect_ration}-{rim_dia}",
                    "twi": twi,
                    "load_index": load_index,
                    "speed_rating": speed_rating,
                    "tubing": tubing,
                    "tread_pattern": tread_pattern,
                }
                db_handler.load_database("SpecsDB")
                db_handler.load_collection("tyre")
                result = db_handler.add_document_to_collection(new_tyre_document)
                if result == 1:
                    st.success("Document saved to Database successfully!")
                else:
                    st.error("Error saving document to MongoDB.")