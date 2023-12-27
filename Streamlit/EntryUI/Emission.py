import streamlit as st
from Misc import get_html_report
from DBOps import crud_operations
import pandas as pd
from pymongo import MongoClient
from DataTools import StringTools
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotting_package import plotly_tools

def emission_entry():
    pass


def emission_analysis_ui():
    etr1 = st.text_input("ETR 1", key="etr_1")
    # etr2 = st.text_input("ETR 2", key="etr_2")
    if st.button("GET REPORT"):
        etr_no_required = [etr1]
        fig = get_html_report.html_report(etr_no_required,
                     inca_variables_additional=[],
                     wmtc_class_list=[],
                     remark_dict={},
                     remark_entries=[],
                     ltheme=0,
                     smooth=0,
                     ecarb=0,
                     vdpl=1,
                     tid=0,
                     call="html_report",
                     unit="g/s"
                     )

        # st.plotly_chart(fig)
        # html_file_path = r"D:\BAL Projects\01_Misc\MN_Colab\Streamlit\data\ETR REPORT NO 860.html"
        # fig = pio.read_html(html_file_path)[0]
        # st.components.v1.html(open(html_file_path, 'r').read(), width=800, height=600)
        st.plotly_chart(fig)


def emission_dashboard_2w():
    # client = MongoClient("mongodb://localhost:27017/")
    # client = MongoClient("mongodb://10.11.10.95:27017/")
    # st.title("EMISSION DASHBOARD")
    # bosch_tab, vdpl_tab = st.tabs(["BOSCH", "VDPL"])
    # datahandler = crud_operations.MongoDBHandler(client)
    # datahandler.load_database("testing_history")
    # datahandler.load_collection("emission_dashboard")
    # with bosch_tab:
    #     pipeline = [
    #         {
    #             "$group": {
    #                 "_id": {
    #                     "model": "$MODEL",
    #                     "result": "$RESULT"
    #                 },
    #                 "count": {"$sum": 1}
    #             }
    #         },
    #         {
    #             "$match": {
    #                 "_id.result": {"$in": ["PASS", "FAIL"]}
    #             }
    #         }
    #     ]
    #
    #     result = list(datahandler.collection.aggregate(pipeline))
    #     data = {"model": [], "result": [], "count": []}
    #     for item in result:
    #         data["model"].append(item["_id"]["model"])
    #         data["result"].append(item["_id"]["result"])
    #         data["count"].append(item["count"])
    #     df = pd.DataFrame(data)
    #     df = df.sort_values(by="model")
    #     df['model'] = df['model'].apply(StringTools.remove_unnecessary_characters)
    #
    #     print("OK")
    def load_df(file_path):
        df = pd.read_csv(file_path)
        return df

    def get_models(df):
        model_names = ["All Models"] + list(df["MODEL"].unique())
        return model_names

    def get_test_counts(filtered_df):
        result = {
        "Total Tests": len(filtered_df),
        "Passed": len(filtered_df[filtered_df["RESULT"] == "PASS"]),
        "Failed": len(filtered_df[filtered_df["RESULT"] == "FAIL"]),
        }
        return result

    def get_filtered_df_based_on_time(time_delta):
        end_date = max(df["DATE"])
        start_date = end_date - timedelta(days=time_delta)
        filtered_data = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]
        return filtered_data

    def get_test_count_bar_plot(filtered_df, model="all"):
        if model == "all":
            data = filtered_df.groupby("MODEL")["RESULT"].value_counts().unstack().fillna(0)
            colors = {'Pass': 'blue', 'Fail': 'red'}
            fig = px.bar(data, orientation='h', barmode='stack', color_discrete_map=colors)
            fig.update_layout(xaxis_tickangle=-45, )  # Adjust the angle of x-axis tick labels
            return fig

    def sunburst_plot(filtered_df, levels, color_level):
        fig_sunburst = px.sunburst(
            filtered_df,
            path=levels,
            color=color_level,
            title='Sunburst Chart',
            color_discrete_map={'PASS': 'green', 'FAIL': 'red'}
        )

        return fig_sunburst

    def all_models_weekly(filtered_df):
        test_counts = get_test_counts(filtered_df)
        c1, c2, c3 = st.columns(3)
        for col, key, val in zip([c1, c2, c3], test_counts.keys(), test_counts.values()):
            col.metric(key, val)
        st.plotly_chart(get_test_count_bar_plot(filtered_df), use_container_width=True)

        ems_sunburst = plotly_tools.PlotBuilder(filtered_df)
        ems_sunburst.sunburst_plot(levels=["EMS", "MODEL", "RESULT", "category"],
                                   color_level="category")
        st.plotly_chart(ems_sunburst.fig, use_container_width=True)


    def single_model_weekly(model_name):
        pass

    st.title("EMISSION DASHBOARD")
    file_path = "data/emission_csv/single_line_csv_etr_entry.csv"

    df = load_df(file_path)
    df["DATE"] = pd.to_datetime(df["DATE"], format='%d/%m/%Y')
    selected_model = st.sidebar.selectbox("Select Model Name:", get_models(df))

    wk_tab, hist_tab = st.tabs(["WEEKLY", "HISTORICAL"])
    if selected_model == "All Models":
        with wk_tab:
            filtered_df = get_filtered_df_based_on_time(time_delta=6)
            all_models_weekly(filtered_df)

    else:
        single_model_weekly(selected_model)






