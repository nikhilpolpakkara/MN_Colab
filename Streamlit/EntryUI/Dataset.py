import streamlit as st
import datetime
from DBOps import MongoDBOps
import pandas as pd
from plotting_package import plotly_tools
from DataTools import DfTools
import os

line_color = "#2a9df4"

def add_new_project():
    pass

def add_dataset():
    pass

def get_project_list():
    return ['K403','T400','K17']

def get_dataset_list(selected_model):
    return ["D1", "D2", "D3"]

def get_df(client,project_id):
    # print(project_id)
    dataset_history_handler = crud_operations.MongoDBHandler(client)
    dataset_history_handler.load_database("CAL")
    dataset_history_handler.load_collection("dataset_log")
    dataset_hist = dataset_history_handler.get_field_values_from_level_1_collection(
        field_names=["date",
                     "project_name",
                     "dataset_name",
                     "parent_dataset_name",
                     "dataset_comments",
                     "functions_changed",
                     "variables_changed"],
        collection_filter={
            "project_id": project_id,
        }
    )
    dataset_hist = pd.DataFrame(dataset_hist)
    return dataset_hist

def dataset_entry(client):
    st.title(f":blue[DATASET REVIEW]")
    selected_model = st.selectbox("Select Project", [ "K17", "K403", "Add new Model",])
    def disable():
        st.session_state.disabled = True

    def enable():
        st.session_state.disabled = False
    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    if not selected_model == "Add new Model":
        tab1, tab2, tab3= st.tabs(["Update Dataset", "Dataset History", "Add comments"])
        with tab1:
            with st.expander("UPLOAD DATASET FILES"):
                dataset_list = ["Select parent dataset"] + get_dataset_list("model")
                parent_dataset = st.selectbox("Choose Dataset", dataset_list)
                upload_hex_file = st.file_uploader("Choose a HEX file", type=["hex"])
                upload_a2l_file = st.file_uploader("Choose a a2L file", type=["a2L"])
                upload_DCM_file = st.file_uploader("Choose a DCM file", type=["DCM"], accept_multiple_files=True)
                upload_cvx_file = st.file_uploader("Choose a cvx file", type=["cvx"])
                # st.header("Enter remark")

                dataset_review = st.button("REVIEW DATASET CHANGES", use_container_width=True)

            if dataset_review:
                with st.form("REVIEW DATASET CHANGES"):
                    st.subheader("FUNCTION-WISE DATASET CHANGES")
                    changes_df = pd.read_excel(os.path.abspath("data/changes_df.xlsx"))
                    with st.expander("Function 1"):
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.text("Variable")
                            st.text("Variable 1")
                            # st.text("V2")
                            # st.text("V3")
                            # st.text("V4")
                        with c2:
                            st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_1")
                            # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_2")
                            # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_3")
                            # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_4")

                        with c3:
                            st.selectbox("priority", ["Low", "Medium", "High"], key="priority_1")
                            # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_2")
                            # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_3")
                            # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_5")

                        with c4:
                            notes = st.text_input("Comment", key="comment_f1_1")
                            # notes = st.text_input("Comment")
                            # notes = st.text_input("Comment")
                            # notes = st.text_input("Comment")

                    with st.expander("Function 2"):
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            st.text("Variable")
                            st.text("Variable 1")
                            # st.text("V2")
                            # st.text("V3")
                            # st.text("V4")
                        with c2:
                            st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_f2_1")
                            # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_2")
                            # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_3")
                            # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_4")

                        with c3:
                            st.selectbox("priority", ["Low", "Medium", "High"], key="priority_f2__1")
                            # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_2")
                            # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_3")
                            # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_5")

                        with c4:
                            notes = st.text_input("Comment", key="comment_f2_1")
                            # notes = st.text_input("Comment")
                            # notes = st.text_input("Comment")
                            # notes = st.text_input("Comment")

                    dataset_upload = st.form_submit_button("SUBMIT DATASET", use_container_width=True)


        with tab2:
            df = get_df(client, selected_model)
            st.write(df)

        with tab3:
            selected_dataset = st.selectbox("Choose Dataset",get_dataset_list("model"))
            discussions = st.text_area("Add notes:", "")

        # c = st.chat_input("chat")

    else:
        tab1, tab2 = st.tabs(["Add new project", 'Preview specsheet'])
        with tab1:
            with st.form("project_form"):
                make = st.text_input("Project name")
                upload_spec_file = st.file_uploader("Choose project specsheet", type=["xlsx"])
                base_hex_file = st.file_uploader("Choose a HEX file", type=["hex"])
                base_a2l_file = st.file_uploader("Choose a a2L file", type=["a2L"])
                base_DCM_file = st.file_uploader("Choose a DCM file", type=["DCM"],accept_multiple_files=True)
                base_cvx_file = st.file_uploader("Choose a cvx file", type=["cvx"])
                project_submit = st.form_submit_button("Submit")

        with tab2:
            pass

def dataset_discussion():
    st.title(f":blue[Dataset Discussion]")
    selected_model = st.selectbox("Select Project", ["K17", "K403", "Add new Model", ])
    selected_dataset = st.selectbox("Choose Dataset", get_dataset_list("model"))
    chat = st.chat_input("chat")
