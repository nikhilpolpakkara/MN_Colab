import streamlit as st
import datetime
from DBOps import crud_operations
import pandas as pd
from plotting_package import plotly_tools
from DataTools import DfTools

line_color = "#2a9df4"

def add_new_project():
    pass

def add_dataset():
    pass

def get_project_list():
    return ['K403','T400','K17']

def get_dataset_list(selected_model):
    return ["D1", "D2", "D3"]

def dataset_entry():
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
            select_project = st.selectbox("Select Project", get_project_list())
            upload_hex_file = st.file_uploader("Choose a HEX file", type=["hex"])
            upload_a2l_file = st.file_uploader("Choose a a2L file", type=["a2L"])
            upload_DCM_file = st.file_uploader("Choose a DCM file", type=["DCM"], accept_multiple_files=True)
            upload_cvx_file = st.file_uploader("Choose a cvx file", type=["cvx"])
            # st.header("Enter remark")
            notes = st.text_area("Add your notes here:", "")

        with tab2:
            pass

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
    st.title(f":blue[KARO BAKCHODI]")
    selected_model = st.selectbox("Select Project", ["K17", "K403", "Add new Model", ])
    selected_dataset = st.selectbox("Choose Dataset", get_dataset_list("model"))
    chat = st.chat_input("chat")
