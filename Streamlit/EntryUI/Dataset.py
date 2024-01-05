import streamlit as st
from DBOps import MongoDBOps
from DataTools import misc
import pandas as pd
from cal import cal_common
import os

line_color = "#2a9df4"


def add_new_project():
    pass


def add_dataset():
    pass


def get_project_list(dataset_history_handler):
    project_list = dataset_history_handler.get_field_values_from_level_1_collection(field_names=["project_id"])
    return project_list


def get_dataset_list(dataset_handler):
    dataset_list = dataset_handler.get_field_values_from_level_1_collection(field_names=["dataset_id"])
    return dataset_list


def get_dataset_history_df(client, project_id):
    # print(project_id)
    dataset_history_handler = MongoDBOps.MongoDBHandler(client)
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

    dataset_handler = MongoDBOps.MongoDBHandler(client)
    dataset_handler.load_database("CAL")
    dataset_handler.load_collection("DATASETS")

    dataset_history_handler = MongoDBOps.MongoDBHandler(client)
    dataset_history_handler.load_database("CAL")
    dataset_history_handler.load_collection("dataset_log")

    st.title(f":blue[DATASET REVIEW]")
    project_list = get_project_list(dataset_history_handler)
    selected_model = st.selectbox(label="PROJECT",
                                  options=project_list + ["Add new Model"],
                                  placeholder="Select Project",
                                  index=None
                                  )

    if not selected_model == "Add new Model":
        tab1, tab2, tab3 = st.tabs(["Update Dataset", "Dataset History", "Add comments"])
        with tab1:
            with st.expander("UPLOAD DATASET FILES"):
                dataset_list = get_dataset_list(dataset_handler)
                base_dataset = st.selectbox(
                    label="BASE DATASET",
                    options=["New Software"] + dataset_list,
                    index=None,
                    placeholder="Select Base Dataset"
                )
                if base_dataset == "New Software":
                    external_parent_dataset = st.selectbox(
                        label="SELECT PARENT DATASET",
                        options=dataset_list,
                        placeholder="Select Parent Dataset",
                        index=None
                    )

                current_hex_file = st.file_uploader("Choose Current HEX file", type=["hex"])
                current_cvx_file = st.file_uploader("Choose Current cvx file", type=["cvx"])
                if base_dataset == "New Software":
                    current_a2l_file = st.file_uploader("Choose New Software a2L file", type=["a2L"])
                    current_a2l_step = st.text_input("Please Specify the Software Step")

                external_import = st.radio("Have you imported from other datasets or DCM's ?", options=["No", "Yes"], horizontal=True)
                if external_import == "Yes":
                    external_dcms = st.file_uploader("Choose DCM files", type=["DCM"], accept_multiple_files=True)
                    external_datasets = st.multiselect(
                        label="Select Other Datasets from where Values are imported",
                        options=dataset_list,
                        placeholder="Select Datasets"
                    )

                container = st.radio("Are you going to send this dataset for container ?", options=["No", "Yes"], horizontal=True)
                if container == "Yes":
                    container_id = st.text_input(label="Please enter dataset part no")

                dataset_review = st.button("REVIEW DATASET CHANGES", use_container_width=True)

            if dataset_review:
                pass
                # with st.form("REVIEW DATASET CHANGES"):
                #     st.subheader("FUNCTION-WISE DATASET CHANGES")
                #     changes_df = pd.read_excel(os.path.abspath("data/changes_df.xlsx"))
                #     with st.expander("Function 1"):
                #         c1, c2, c3, c4 = st.columns(4)
                #         with c1:
                #             st.text("Variable")
                #             st.text("Variable 1")
                #             # st.text("V2")
                #             # st.text("V3")
                #             # st.text("V4")
                #         with c2:
                #             st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_1")
                #             # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_2")
                #             # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_3")
                #             # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_4")
                #
                #         with c3:
                #             st.selectbox("priority", ["Low", "Medium", "High"], key="priority_1")
                #             # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_2")
                #             # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_3")
                #             # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_5")
                #
                #         with c4:
                #             notes = st.text_input("Comment", key="comment_f1_1")
                #             # notes = st.text_input("Comment")
                #             # notes = st.text_input("Comment")
                #             # notes = st.text_input("Comment")
                #
                #     with st.expander("Function 2"):
                #         c1, c2, c3, c4 = st.columns(4)
                #         with c1:
                #             st.text("Variable")
                #             st.text("Variable 1")
                #             # st.text("V2")
                #             # st.text("V3")
                #             # st.text("V4")
                #         with c2:
                #             st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_f2_1")
                #             # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_2")
                #             # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_3")
                #             # st.selectbox("category", ["CAL", "DCM", "Hardware", "Other Dataset"], key="category_4")
                #
                #         with c3:
                #             st.selectbox("priority", ["Low", "Medium", "High"], key="priority_f2__1")
                #             # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_2")
                #             # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_3")
                #             # st.selectbox("priority", ["Low", "Medium", "High"], key="priority_5")
                #
                #         with c4:
                #             notes = st.text_input("Comment", key="comment_f2_1")
                #             # notes = st.text_input("Comment")
                #             # notes = st.text_input("Comment")
                #             # notes = st.text_input("Comment")
                #
                #     dataset_upload = st.form_submit_button("SUBMIT DATASET", use_container_width=True)

        with tab2:
            df = get_dataset_history_df(client, selected_model)
            st.write(df)

        with tab3:
            selected_dataset = st.selectbox("Choose Dataset", dataset_list)
            discussions = st.text_area("Add notes:", "")

        # c = st.chat_input("chat")

    else:
        tab1, tab2 = st.tabs(["Add new project", 'Preview specsheet'])
        with tab1:
            with st.form("NEW PROJECT FORM"):
                new_project_id = st.text_input("PROJECT ID")
                new_project_name = st.text_input("PROJECT NAME")
                new_project_family = st.selectbox("FAMILY", ["pulsar", "dominor", "platina", "triumph", "ktm"], index=None)
                new_project_ems = st.selectbox("EMS", ["bosch", "vdpl", "mikuni", "bal"], index=None)
                new_project_spec_file = st.file_uploader("Choose project specsheet", type=["xlsx"])
                submit_new_project = st.form_submit_button("SUBMIT", use_container_width=True)
                cal_paths = cal_common.CalPaths()
                if submit_new_project:
                    destination_path_for_spec_file = cal_paths.h1_calibration_path + f"/00_BRANDS/{new_project_family}/{new_project_id}/00_SpecSheet/{new_project_spec_file.name}"
                    misc.create_directory_along_path(os.path.dirname(destination_path_for_spec_file))
                    misc.copy_streamlit_file_to_location(new_project_spec_file, destination_path_for_spec_file)

                    new_project_doc = {
                        "project_id": new_project_id,
                        "project_name": new_project_name,
                        "ems": new_project_ems,
                        "spec_file_path": destination_path_for_spec_file,
                        "dataset_history": []
                    }
                    dataset_history_handler.add_document_to_collection(new_project_doc)

        with tab2:
            pass


def dataset_discussion():
    st.title(f":blue[Dataset Discussion]")
    selected_model = st.selectbox("Select Project", ["K17", "K403", "Add new Model", ])
    selected_dataset = st.selectbox("Choose Dataset", get_dataset_list("model"))
    chat = st.chat_input("chat")
