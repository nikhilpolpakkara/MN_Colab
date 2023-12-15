import streamlit as st
import datetime
from MongoDBOps import crud_operations
import pandas as pd
from plotting_package import plotly_tools
from DataTools import DfTools

line_color = "#2a9df4"


def add_new_vehicle():
    print("Taking you to add vehicle page")
    with st.form("vehicle_form"):
        model = st.selectbox("Model", options=[])
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


def test_data_entry(department_name, test_activity_name, client):
    st.title(f":blue[TYRE WEAR]")

    def disable():
        st.session_state.disabled = True

    def enable():
        st.session_state.disabled = False
    if "disabled" not in st.session_state:
        st.session_state.disabled = False
        
    def fill_vehicle_details():
        if not st.session_state["veh_id"] == "new vehicle":
            print("Fetching Vehicle Details")
            vehicle_details = vehicle_details_handler.get_document_from_level_1_collection(
                document_filter={"_id": st.session_state["veh_id"]},
            )
            st.session_state["model"] = vehicle_details["model"]
            st.session_state["chassis_no"] = vehicle_details["chassis_no"]
            st.session_state["batch"] = vehicle_details["batch"]
        else:
            add_new_vehicle()

    dept_details_handler = crud_operations.MongoDBHandler(client)
    dept_details_handler.load_database("common")
    dept_details_handler.load_collection("department_details")

    test_activity_doc = dept_details_handler.get_document_from_level_2_collection(
        collection_filter={'name': department_name},
        nested_array="test_activity",
        array_document_filter={"field_name": 'name', "field_value": test_activity_name}
    )
    test_id = test_activity_doc["test_id"]
    tab1, tab2, tab3 = st.tabs(["Test Data Entry", "Add New tyre", "Tyre Catalogue"])

    vehicle_details_handler = crud_operations.MongoDBHandler(client)
    vehicle_details_handler.load_database("testing_history")
    vehicle_details_handler.load_collection("vehicle_testing")

    options_dict = {
        "veh_id": vehicle_details_handler.get_field_values_from_level_1_collection(field_names=["_id"], project_id=True),
    }

    test_data_handler = crud_operations.MongoDBHandler(client)
    test_data_handler.load_database("testing_data")
    test_data_handler.load_collection(test_id)

    with tab1:
        veh_id = st.selectbox(
            "VEH ID".upper(),
            key="veh_id",
            options=options_dict["veh_id"] + ["new vehicle"],
            index=None,
            on_change=fill_vehicle_details
        )
        with st.form("tyrewear_form"):
            with st.expander("BASIC DETAILS"):
                date = st.date_input("SELECT DATE", datetime.datetime.now().date(), key="date")
                engineer = st.text_input("ENGINEER*")
            with st.expander("VEHICLE DETAILS"):
                model = st.text_input("MODEL", key="model")
                chassis_no = st.text_input("CHASSIS NO", key="chassis_no")
                batch = st.text_input("BATCH", key="batch")

            odo_reading = st.number_input("ODO READING", step=1, value=None)
            st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)
            st.subheader("FRONT TYRE ENTRY")

            with st.expander("TYRE DETAILS"):
                f_tyre_id = st.number_input("TYRE ID", key="f_tyre_id", value=None)

            with st.expander("TYRE HISTORY"):
                f_tyre_replace_odo = st.number_input("TYRE REPLACE ODO", key="f_tyre_replace_odo", value=None, step=1)
                f_tyre_run_km = st.number_input("TYRE RUNNING", value=None, key="f_tyre_run_km" ,step=1)

            with st.expander("TYRE WEAR MEASUREMENTS"):
                f_lh_c, f_rh_c, f_c_c = st.columns(3)

                with f_lh_c:
                    f_lh1 = st.number_input("LH1", key="f_lh1", value=None)
                    f_lh2 = st.number_input("LH2", key="f_lh2", value=None)
                    f_lh3 = st.number_input("LH3", key="f_lh3", value=None)
                    f_lh4 = st.number_input("LH4", key="f_lh4", value=None)
                    f_lh5 = st.number_input("LH5", key="f_lh5", value=None)
                    f_lh6 = st.number_input("LH6", key="f_lh6", value=None)

                with f_rh_c:
                    f_rh1 = st.number_input("RH1", key="f_rh1", value=None)
                    f_rh2 = st.number_input("RH2", key="f_rh2", value=None)
                    f_rh3 = st.number_input("RH3", key="f_rh3", value=None)
                    f_rh4 = st.number_input("RH4", key="f_rh4", value=None)
                    f_rh5 = st.number_input("RH5", key="f_rh5", value=None)
                    f_rh6 = st.number_input("RH6", key="f_rh6", value=None)

                with f_c_c:
                    f_c1 = st.number_input("C1", key="f_c1", value=None)
                    f_c2 = st.number_input("C2", key="f_c2", value=None)
                    f_c3 = st.number_input("C3", key="f_c3", value=None)
                    f_c4 = st.number_input("C4", key="f_c4", value=None)
                    f_c5 = st.number_input("C5", key="f_c5", value=None)
                    f_c6 = st.number_input("C6", key="f_c6", value=None)

                f_twi1 = st.number_input("TWI1", key="f_twi1", value=None)
                f_twi2 = st.number_input("TWI2", key="f_twi2", value=None)
                f_twi3 = st.number_input("TWI3", key="f_twi3", value=None)
                f_tc = st.number_input("TC", key="f_tc", value=None)

            st.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)
            st.subheader("REAR TYRE ENTRY")

            with st.expander("TYRE DETAILS"):
                r_tyre_id = st.number_input("TYRE ID", key="r_tyre_id", value=None)

            with st.expander("TYRE HISTORY"):
                r_tyre_replace_odo = st.number_input("TYRE REPLACE ODO", value=None, key="r_tyre_replace_odo", step=1)
                r_tyre_run_km = st.number_input("TYRE RUNNING", value=None, key="r_tyre_run_km", step=1)

            with st.expander("TYRE WEAR MEASUREMENTS"):
                r_lh_c, r_rh_c, r_c_c = st.columns(3)

                with r_lh_c:
                    r_lh1 = st.number_input("LH1", key="r_lh1", value=None)
                    r_lh2 = st.number_input("LH2", key="r_lh2", value=None)
                    r_lh3 = st.number_input("LH3", key="r_lh3", value=None)
                    r_lh4 = st.number_input("LH4", key="r_lh4", value=None)
                    r_lh5 = st.number_input("LH5", key="r_lh5", value=None)
                    r_lh6 = st.number_input("LH6", key="r_lh6", value=None)

                with r_rh_c:
                    r_rh1 = st.number_input("RH1", key="r_rh1", value=None)
                    r_rh2 = st.number_input("RH2", key="r_rh2", value=None)
                    r_rh3 = st.number_input("RH3", key="r_rh3", value=None)
                    r_rh4 = st.number_input("RH4", key="r_rh4", value=None)
                    r_rh5 = st.number_input("RH5", key="r_rh5", value=None)
                    r_rh6 = st.number_input("RH6", key="r_rh6", value=None)

                with r_c_c:
                    r_c1 = st.number_input("C1", key="r_c1", value=None)
                    r_c2 = st.number_input("C2", key="r_c2", value=None)
                    r_c3 = st.number_input("C3", key="r_c3", value=None)
                    r_c4 = st.number_input("C4", key="r_c4", value=None)
                    r_c5 = st.number_input("C5", key="r_c5", value=None)
                    r_c6 = st.number_input("C6", key="r_c6", value=None)

                r_twi1 = st.number_input("TWI1", key="r_twi1", value=None)
                r_twi2 = st.number_input("TWI2", key="r_twi2", value=None)
                r_twi3 = st.number_input("TWI3", key="r_twi3", value=None)
                r_tc = st.number_input("TC", key="r_tc", value=None)

            submitted = st.form_submit_button("SAVE TEST DATA",
                                              use_container_width=True,
                                              on_click=disable,
                                              disabled=st.session_state.disabled
                                              )
            if submitted:
                f_lh = min([f_lh1, f_lh2, f_lh3, f_lh4, f_lh5, f_lh6]),
                f_rh = min([f_rh1, f_rh2, f_rh3, f_rh4, f_rh5, f_rh6]),
                f_c = min([f_c1, f_c2, f_c3, f_c4, f_c5, f_c6]),
                f_nsd = min([f_lh, f_rh, f_c])

                r_lh = min([r_lh1, r_lh2, r_lh3, r_lh4, r_lh5, r_lh6]),
                r_rh = min([r_rh1, r_rh2, r_rh3, r_rh4, r_rh5, r_rh6]),
                r_c = min([r_c1, r_c2, r_c3, r_c4, r_c5, r_c6]),
                r_nsd = min([r_lh, r_rh, r_c])

                db_handler = crud_operations.MongoDBHandler(client)
                db_handler.load_database("common")
                db_handler.load_collection("counter")
                test_no = db_handler.get_next_id(counter="tyre_wear_test_counter")

                f_data = {
                    "test_no": test_no,
                    "veh_id": veh_id,
                    "tyre_location": "front",
                    "tyre_id": f_tyre_id,
                    "odo_reading": odo_reading,
                    "tyre_replace_odo": f_tyre_replace_odo,
                    "tyre_running": f_tyre_run_km,
                    "engineer": engineer,
                    "lh1": f_lh1,
                    "lh2": f_lh2,
                    "lh3": f_lh3,
                    "lh4": f_lh4,
                    "lh5": f_lh5,
                    "lh6": f_lh6,
                    "lh": f_lh,
                    "rh1": f_rh1,
                    "rh2": f_rh2,
                    "rh3": f_rh3,
                    "rh4": f_rh4,
                    "rh5": f_rh5,
                    "rh6": f_rh6,
                    "rh": f_rh,
                    "c1": f_c1,
                    "c2": f_c2,
                    "c3": f_c3,
                    "c4": f_c4,
                    "c5": f_c5,
                    "c6": f_c6,
                    "c": f_c,
                    "twi1": f_twi1,
                    "twi2": f_twi2,
                    "twi3": f_twi3,
                    "tc": f_tc,
                    "nsd": f_nsd,
                    "date": date.strftime('%d-%m-%Y'),
                    "date_time": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                }

                r_data = {
                    "test_no": test_no,
                    "veh_id": veh_id,
                    "tyre_location": "rear",
                    "tyre_id": r_tyre_id,
                    "odo_reading": odo_reading,
                    "tyre_replace_odo": r_tyre_replace_odo,
                    "tyre_running": r_tyre_run_km,
                    "engineer": engineer,
                    "lh1": r_lh1,
                    "lh2": r_lh2,
                    "lh3": r_lh3,
                    "lh4": r_lh4,
                    "lh5": r_lh5,
                    "lh6": r_lh6,
                    "lh": r_lh,
                    "rh1": r_rh1,
                    "rh2": r_rh2,
                    "rh3": r_rh3,
                    "rh4": r_rh4,
                    "rh5": r_rh5,
                    "rh6": r_rh6,
                    "rh": r_rh,
                    "c1": r_c1,
                    "c2": r_c2,
                    "c3": r_c3,
                    "c4": r_c4,
                    "c5": r_c5,
                    "c6": r_c6,
                    "c": r_c,
                    "twi1": r_twi1,
                    "twi2": r_twi2,
                    "twi3": r_twi3,
                    "tc": r_tc,
                    "nsd": r_nsd,
                    "date": date.strftime('%d-%m-%Y'),
                    "date_time": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                }

                test_data_handler.add_document_to_collection(f_data)
                test_data_handler.add_document_to_collection(r_data)
                vehicle_details_handler.append_to_list_by_id(veh_id, "test_history", f"{test_id}_{test_no}")

        st.button("ENTER NEW DATA",
                  use_container_width=True,
                  on_click=enable,
                  disabled=False
                  )

    with tab2:
        with st.form("tyre_form"):
            tyre_location = st.selectbox("Wheel Postion", options=["front", "rear"], index=None)
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
                db_handler = crud_operations.MongoDBHandler(client)
                db_handler.load_database("common")
                db_handler.load_collection("counter")
                tyre_id = db_handler.get_next_id(counter="tyre_id")
                new_tyre_document = {
                    "_id": tyre_id,
                    "tyre_location": tyre_location,
                    "make": make,
                    "section_width": section_width,
                    "aspect_ratio": aspect_ration,
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
                    st.success("New Tyre Added to Database")
                else:
                    st.error("Error saving document to MongoDB.")

    with tab3:
        tyre_details_handler = crud_operations.MongoDBHandler(client)
        tyre_details_handler.load_database("SpecsDB")
        tyre_details_handler.load_collection("tyre")
        df = tyre_details_handler.get_collection_dataframe()
        st.write(df)


def tyre_wear_analytics(selected_department, client):
    def load_data_handlers():
        veh_details_data_handler = crud_operations.MongoDBHandler(client)
        veh_details_data_handler.load_database("testing_history")
        veh_details_data_handler.load_collection("vehicle_testing")

        test_data_handler = crud_operations.MongoDBHandler(client)
        test_data_handler.load_database("testing_data")
        test_data_handler.load_collection("du_1")
        return veh_details_data_handler, test_data_handler

    def get_df():
        nsd = test_data_handler.get_field_values_from_level_1_collection(
            field_names=["odo_reading", "nsd", "tyre_location", "lh", "rh", "c"],
            collection_filter={
                "veh_id": veh_id,
            }
        )
        nsd = pd.DataFrame(nsd)
        nsd["odo_reading"] = nsd["odo_reading"].astype(float)
        nsd.apply(pd.to_numeric, errors='coerce')
        return nsd

    def generate_derived_columns(group_df):
        group_df["wear"] = -(group_df["nsd"] - group_df["nsd"].max())
        group_df["wear_rate"] = (group_df["wear"] / group_df["odo_reading"]) * 10000
        group_df["extrapolated_life"] = ((group_df["nsd"].max()/(group_df["wear_rate"]/10000)) - group_df["odo_reading"]).__round__(0)
        return group_df

    def load_and_transform():
        df = get_df()
        df = df.groupby('tyre_location').apply(generate_derived_columns).reset_index(drop=True)
        return df

    def get_nsd_trend():
        nsd_trend = plotly.PlotBuilder(df[["odo_reading", "nsd", "tyre_location"]])
        nsd_trend.get_go_line(x="odo_reading", y="nsd", group_by="tyre_location")
        nsd_trend.set_title("NSD TREND")
        nsd_trend.set_x_axis_title("ODO READING(Km)")
        nsd_trend.set_y_axis_title("NSD(mm)")
        return nsd_trend.fig

    def get_wear_rate_trend():
        wear_rate_trend = plotly.PlotBuilder(df[["odo_reading", "wear_rate", "tyre_location"]])
        wear_rate_trend.get_go_line(x="odo_reading", y="wear_rate", group_by="tyre_location")
        wear_rate_trend.set_title("WEAR RATE TREND")
        wear_rate_trend.set_x_axis_title("ODO READING(Km)")
        wear_rate_trend.set_y_axis_title("WEAR RATE (mm/10000 Km)")
        return wear_rate_trend.fig

    def get_spatial_trend(group_df):
        spatial_trend = plotly.PlotBuilder(group_df[["odo_reading", "lh", "rh", "c"]])
        spatial_trend.get_go_line(x="odo_reading", y=["lh", "rh", "c"])
        spatial_trend.set_x_axis_title("ODO READING(Km)")
        spatial_trend.set_y_axis_title("NSD(mm)")
        return spatial_trend

    def get_tyre_life_trend():
        tyre_life_trend = plotly.PlotBuilder(df[["odo_reading", "extrapolated_life", "tyre_location"]])
        tyre_life_trend.get_go_line(x="odo_reading", y="extrapolated_life", group_by="tyre_location")
        tyre_life_trend.set_title("TYRE LIFE TREND")
        tyre_life_trend.set_x_axis_title("ODO READING(Km)")
        tyre_life_trend.set_y_axis_title("TYRE LIFE (Km)")
        return tyre_life_trend.fig

    # st.title("TYRE WEAR ANALYSIS")
    veh_details_data_handler, test_data_handler = load_data_handlers()

    veh_id = st.selectbox(
        label="VEHICLE NO",
        options=veh_details_data_handler.get_field_values_from_level_1_collection(
            field_names=["_id"],
            project_id=True
        )
    )

    df = load_and_transform()
    nsd_trend = get_nsd_trend()
    st.plotly_chart(nsd_trend)

    wear_rate_trend = get_wear_rate_trend()
    st.plotly_chart(wear_rate_trend)

    spatial_trend = df.groupby("tyre_location").apply(get_spatial_trend)
    for group_name, trend in spatial_trend.items():
        print(group_name)
        trend.set_title(f"{group_name.upper()} TYRE WEAR: Right/Left/Centre")
        st.plotly_chart(trend.fig)

    tyre_life_trend = get_tyre_life_trend()
    st.plotly_chart(tyre_life_trend)

    st.write(df)

    
