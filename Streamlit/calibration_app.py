import streamlit as st
from pymongo import MongoClient
from EntryUI import Emission
from streamlit_tree_select import tree_select
from EntryUI import Dataset

line_color = "#2a9df4"


@st.cache_resource(ttl="30s")
def load_connection():
    print("Establishing Database Connection")
    # client = MongoClient("mongodb://localhost:27017/")
    # client = MongoClient("mongodb://10.11.10.95:27017/")
    client = MongoClient("mongodb://10.11.10.9:27017/")
    # client = MongoClient("mongodb://10.11.10.72:27017/")
    # client = MongoClient("mongodb+srv://nikhilpolpakkara:Aspire_13@cluster0.4cun9lz.mongodb.net/?retryWrites=true&w=majority")
    return client


# Main App
def main():
    print("----------------Starting app----------------")

    print("loading sidebar")
    st.sidebar.title("CALIBRATION APP")
    st.sidebar.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)
    client = load_connection()

    nodes = [

                {
                    "label": "DASHBOARD",
                    "value": "cal_dashboard",
                    "children": [
                        {
                            "label": "2W EMISSION DASHBOARD",
                            "value": "emission_dashboard_2w"
                        },
                        {
                            "label": "3WD EMISSION DASHBOARD",
                            "value": "emission_dashboard_3wd"
                        }
                    ]
                },
                {
                    "label": "ANALYTICS",
                    "value": "cal_analytics",
                    "children": [
                        {
                            "label": "EMISSION ANALYSIS",
                            "value": "emission_analysis"
                        }
                    ]
                },
                {
                    "label": "DATA ENTRY",
                    "value": "cal_data_entry",
                    "children": [
                        {
                            "label": "EMISSION ENTRY",
                            "value": "emission_entry"
                        }
                    ]
                },

                {
                    "label": "DOCUMENTATION",
                    "value": "cal_documentation",
                    "children": [
                        {
                            "label": "BASE CAL",
                            "value": "base_cal"
                        }
                    ]
                },
                {
                    "label": "MISC",
                    "value": "cal_misc",
                    "children": [
                        {
                            "label": "DATASET UPLOAD",
                            "value": "dataset_upload"
                        },
                        {
                            "label": "DATASET DISCUSSION",
                            "value": "dataset_discussion"
                        }
                    ]
                },

            ]

    with st.sidebar:
        tree = tree_select(nodes, only_leaf_checkboxes=True)

    checkbox_ticked = list(set(tree["checked"]) - set(tree["expanded"]))
    print(checkbox_ticked)
    if len(checkbox_ticked) == 0:
        # st.error("Please select something")
        st.image(image="data/main_1.png",
                 use_column_width=True,
                 # caption = "WELCOME"
                )

    else:
        if len(checkbox_ticked) > 1:
            st.error("Please select only one option in sidebar")
        else:
            selected_page = checkbox_ticked[0]
            print(selected_page)
            if selected_page == "emission_analysis":
                Emission.emission_analysis_ui()
            elif selected_page == "emission_dashboard_2w":
                Emission.emission_dashboard_2w()
            elif selected_page == 'dataset_upload':
                Dataset.dataset_entry(client)
            elif selected_page == 'dataset_discussion':
                Dataset.dataset_discussion()
            elif selected_page == "emission_dashboard_3wd":
                Emission.emission_dashboard_3wd()


if __name__ == "__main__":
    main()