import streamlit as st
import numpy as np
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
from EntryUI import common
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

    def get_vin(df):
        vin_names = ["All VIN"] + list(df["VIN"].unique())
        return vin_names
    def get_test_counts(filtered_df):
        result = {
        "Total Tests": len(filtered_df),
        "Passed": len(filtered_df[filtered_df["RESULT"] == "PASS"]),
        "Failed": len(filtered_df[filtered_df["RESULT"] == "FAIL"]),
        }
        return result

    def get_filtered_df_based_on_time(df, time_delta=None):
        end_date = max(df["DATE"])
        if time_delta is None:
            start_date = min(df["DATE"])
        else:
            start_date = end_date - timedelta(days=time_delta)
        filtered_data = df[(df["DATE"] >= start_date) & (df["DATE"] <= end_date)]
        return filtered_data

    def get_filtered_df_based_on_vin(df, vin_names):
        filtered_data = df[df['VIN'].isin(vin_names)]
        return filtered_data

    def get_test_count_bar_plot(filtered_df, groupby, model="all"):
        if model == "all":
            data = filtered_df.groupby(groupby)["RESULT"].value_counts().unstack().fillna(0)
            data["total"] = data["PASS"] + data["FAIL"]
            data = data.sort_values(by='total', ascending=True)
            data = data.drop("total", axis=1)
            # colors = {'PASS': 'blue', 'FAIL': 'red'}
            fig = px.bar(data, orientation='h', barmode='stack', text_auto=True)
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

    def get_pollutant_history_for_model(filtered_df):
        selected_columns = ["CO%", "HC%", "NMHC%", "NOX%"]
        colors = common.generate_color_palette(selected_columns)
        filtered_df["Tests"] = pd.Categorical(np.arange(1, len(filtered_df)+1))
        fig_line_chart = go.Figure()

        for i, column in enumerate(selected_columns):
            fig_line_chart.add_trace(
                go.Scatter(
                    x=filtered_df["Tests"],
                    y=filtered_df[column],
                    mode='lines+markers',
                    name=column,
                    line=dict(shape='spline'),
                    marker=dict(color=colors[i]),
                    hovertext=filtered_df["SN"],
                )
            )

        fig_line_chart.update_layout(
            xaxis_title="Tests",
            yaxis_title="%",
        )

        return fig_line_chart

    def get_pollutant_box_plot(filtered_data):
        # Select columns for boxplot
        selected_columns = ["CO%", "HC%", "NMHC%", "NOX%"]
        colors = common.generate_color_palette(selected_columns)
        data = pd.DataFrame({
            'CO%': np.random.randint(0, 150, 100),
            'HC%': np.random.randint(0, 150, 100),
            'NMHC%': np.random.randint(0, 150, 100),
            'NOX%': np.random.randint(0, 150, 100),
        })
        # st.subheader("Combined Boxplot for Selected Model:")
        fig_combined_boxplot = px.box()

        for i, column in enumerate(selected_columns):
            fig_combined_boxplot.add_trace(
                go.Box(y=filtered_data[column],
                       name=f"{column}",
                       marker=dict(color=colors[i])
            )
            )
        # Set y-axis range
        fig_combined_boxplot.update_yaxes(range=[0, 150])

        # Customize layout
        fig_combined_boxplot.update_layout(
            # title=f"Combined Boxplot for {selected_model}",
            xaxis_title="Selected Columns",
            yaxis_title="%",
        )

        return fig_combined_boxplot

    def all_models_daily(filtered_df):
        test_counts = get_test_counts(filtered_df)
        c1, c2, c3 = st.columns(3)
        for col, key, val in zip([c1, c2, c3], test_counts.keys(), test_counts.values()):
            col.metric(key, val)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(get_test_count_bar_plot(
                filtered_df=filtered_df,
                groupby="MODEL"
            ),
                use_container_width=True
            )
        with c2:
            st.plotly_chart(get_test_count_bar_plot(
                filtered_df=filtered_df,
                groupby="VTC"
            ),
                use_container_width=True
            )

        ems_sunburst = plotly_tools.PlotBuilder(filtered_df)
        ems_sunburst.sunburst_plot(levels=["EMS", "MODEL",'RESULT', "category"],
                                   color_level="category"
                                   )
        st.plotly_chart(ems_sunburst.fig, use_container_width=True)

    def single_model_daily(filtered_df):
        test_counts = get_test_counts(filtered_df)
        c1, c2, c3 = st.columns(3)
        for col, key, val in zip([c1, c2, c3], test_counts.keys(), test_counts.values()):
            col.metric(key, val)

    def single_model_weekly(filtered_df):
        test_counts = get_test_counts(filtered_df)
        c4, c5, c6 = st.columns(3)
        for col, key, val in zip([c4, c5, c6], test_counts.keys(), test_counts.values()):
            col.metric(key, val)

    def single_model_historical(filtered_df):
        test_counts = get_test_counts(filtered_df)
        c1, c2, c3 = st.columns(3)
        for col, key, val in zip([c1, c2, c3], test_counts.keys(), test_counts.values()):
            col.metric(key, val)

    st.title("EMISSION DASHBOARD")
    file_path = "data/emission_csv/single_line_csv_etr_entry.csv"

    df = load_df(file_path)
    df["DATE"] = pd.to_datetime(df["DATE"], format='%d/%m/%Y')
    df['VTC'] = "VTC_"+df['VTC'].astype(str)
    selected_model = st.sidebar.selectbox("Select Model Name:", get_models(df))

    if selected_model == "All Models":
        filtered_df = get_filtered_df_based_on_time(df=df, time_delta=1)
        all_models_daily(filtered_df)

    else:
        d_tab, wk_tab, hist_tab = st.tabs(["DAILY","WEEKLY", "HISTORICAL"])

        with d_tab:
            daily_filtered_df = get_filtered_df_based_on_time(df=df,time_delta=1)
            daily_filtered_df = daily_filtered_df[daily_filtered_df["MODEL"] == selected_model]
            single_model_daily(daily_filtered_df)
            # st.plotly_chart(get_pollutant_history_for_model(daily_filtered_df))

        with wk_tab:
            weekly_filtered_df = get_filtered_df_based_on_time(df=df,time_delta=6)
            weekly_filtered_df = weekly_filtered_df[weekly_filtered_df["MODEL"] == selected_model]
            selected_veh = st.selectbox("Select VIN:",
                                        get_vin(weekly_filtered_df),
                                        key='weekly_data',
                                        )

            if selected_veh == "All VIN":
                single_model_weekly(weekly_filtered_df)
                st.plotly_chart(get_pollutant_history_for_model(weekly_filtered_df))
            else:
                weekly_filt_df_vin = get_filtered_df_based_on_vin(weekly_filtered_df,[selected_veh])
                single_model_weekly(weekly_filt_df_vin)
                st.plotly_chart(get_pollutant_history_for_model(weekly_filt_df_vin))

        with hist_tab:

            hist_filtered_df = get_filtered_df_based_on_time(df=df)
            hist_filtered_df = hist_filtered_df[hist_filtered_df["MODEL"] == selected_model]
            selected_veh_hist = st.selectbox("Select VIN:",
                                             get_vin(hist_filtered_df),
                                             key="historical_data",
                                             )
            if selected_veh_hist == "All VIN":
                single_model_historical(hist_filtered_df)
                st.plotly_chart(get_pollutant_box_plot(hist_filtered_df))
            else:
                hist_filtered_vin= get_filtered_df_based_on_vin(hist_filtered_df,
                                               [selected_veh_hist])
                single_model_historical(hist_filtered_vin)
                st.plotly_chart(get_pollutant_box_plot(hist_filtered_vin))
            # st.plotly_chart(get_pollutant_history_for_model(filtered_df))





