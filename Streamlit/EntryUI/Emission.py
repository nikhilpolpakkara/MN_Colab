import streamlit as st
from Misc import get_html_report
from DBOps import crud_operations
import pandas as pd
from pymongo import MongoClient

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
    client = MongoClient("mongodb://localhost:27017/")
    st.title("EMISSION DASHBOARD")
    bosch_tab, vdpl_tab = st.tabs(["BOSCH", "VDPL"])
    datahandler = crud_operations.MongoDBHandler(client)
    datahandler.load_database("testing_history")
    datahandler.load_collection("emission_dashboard")
    with bosch_tab:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "model": "$MODEL",
                        "result": "$RESULT"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "_id.result": {"$in": ["PASS", "FAIL"]}
                }
            }
        ]

        result = list(datahandler.collection.aggregate(pipeline))
        data = {"model": [], "result": [], "count": []}
        for item in result:
            data["model"].append(item["_id"]["model"])
            data["result"].append(item["_id"]["result"])
            data["count"].append(item["count"])
        df = pd.DataFrame(data)
        df = df.sort_values(by="model")
        # # Prepare data for plotting
        # data = {"model": [], "pass_count": [], "fail_count": []}
        #
        # for item in result:
        #     model = item["_id"]["model"]
        #     count = item["count"]
        #
        #
        #     if item["_id"]["result"] == "PASS":
        #         data["pass_count"].append(count)
        #         data["fail_count"].append(0)  # Add 0 for fail count to align with pass counts
        #     elif item["_id"]["result"] == "FAIL":
        #         data["fail_count"][-1] = count  # Update the last fail count
        #
        #     if model not in data["model"]:
        #         data["model"].append(model)

        # Create a DataFrame
        # df = pd.DataFrame(data)
        print("OK")

    vdpl_tab = st.tabs("VDPL")




