import streamlit as st
from DBOps import crud_operations
from DataTools import DictTools
from plotting_package import plotly_tools
from datetime import datetime, timedelta


def plotly_timeline(client):
    print("Loading Timeline")
    datahandler = crud_operations.MongoDBHandler(client)
    datahandler.load_database("testing_history")
    datahandler.load_collection("timeline")
    filters_col, graphs_col = st.columns([1, 3])
    with filters_col:
        st.write("FILTERS")

        start_date = st.date_input("START DATE", datetime.now() - timedelta(days=30), key="start_date")
        end_date = st.date_input("END DATE", datetime.now(), key="end_date")

        selected_models = st.multiselect("MODEL", options=datahandler.get_field_values_from_level_1_collection(["model"]), key="model")
        selected_depts = st.multiselect("DEPARTMENT", options=datahandler.get_field_values_from_level_1_collection(["dept"]), key="dept")
        selected_vehicles = st.multiselect("VEHICLES", options=datahandler.get_field_values_from_level_1_collection(["vehicle"]), key="vehicle")

    with graphs_col:
        filters_dict = st.session_state.to_dict()
        print(filters_dict)
        filters_selected = DictTools.non_empty_lists_fields(filters_dict)
        print(filters_selected)
        if len(filters_selected) == 1:
            if "model" in filters_selected:
                df = datahandler.get_collection_dataframe(
                    collection_filter={"model": filters_dict["model"]},
                    # time_filter={"start_date": start_date.strftime('%d-%m-%Y %H:%M:%S'),
                    #              "end_date": end_date.strftime('%d-%m-%Y %H:%M:%S')},

                )
                plot = plotly_tools.PlotBuilder(df)
                plot.set_column_to_datetime("date")
                plot.get_scatter_timeline(x="date", y="dept", group_by=["dept"], hovertext="test_activity")
                st.plotly_chart(plot.fig)

        if len(filters_selected) == 2:
            if "model" in filters_selected:
                if "dept" in filters_selected:
                    df = datahandler.get_collection_dataframe(
                        collection_filter={"model": filters_dict["model"], "dept": filters_dict["dept"]},
                        # time_filter={"start_date": start_date.strftime('%d-%m-%Y %H:%M:%S'),
                        #              "end_date": end_date.strftime('%d-%m-%Y %H:%M:%S')},

                    )
                    plot = plotly_tools.PlotBuilder(df)
                    plot.set_column_to_datetime("date")
                    plot.get_scatter_timeline(x="date", y="vehicle", group_by=["vehicle"], hovertext="test_activity")
                    st.plotly_chart(plot.fig)

                if "vehicle" in filters_selected:
                    pass




