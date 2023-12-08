import streamlit as st
import datetime
from MongoDBOps import crud_operations

line_color = "#2a9df4"


def test_data_entry(tyre_wear_doc, test_data_handler, client):
    def fill_vehicle_details():
        print("Fetching Vehicle Details")
        vehicle_details = vehicle_details_handler.get_document_from_collection(
            document_filter={"rev_no": st.session_state["veh_id"]}
        )
        st.session_state["model"] = vehicle_details["model"]
        st.session_state["chassis_no"] = vehicle_details["chassis_no"]
        st.session_state["batch"] = vehicle_details["batch"]

    st.title(f":blue[TYRE WEAR]")
    tab1, tab2, tab3 = st.tabs(["Test Data Entry", "Add New Vehicle" ,"Add New tyre"])

    vehicle_details_handler = test_data_handler
    vehicle_details_handler.load_collection("vehicle_details")
    options_dict = {
        "veh_id": vehicle_details_handler.get_field_values_from_collection(field_name="rev_no"),
    }

    with tab1:
        rev_no = st.selectbox(
            "REV NO".upper(),
            key="veh_id",
            options=options_dict["veh_id"],
            index=None,
            on_change=fill_vehicle_details
        )
        with st.form("my_form"):
            with st.expander("BASIC DETAILS"):
                date = st.date_input(
                    "SELECT DATE",
                    datetime.datetime.now().date(),
                    key="date"
                )

                engineer = st.text_input(
                    "ENGINEER*"
                )
            with st.expander("VEHICLE DETAILS"):
                model = st.text_input("")