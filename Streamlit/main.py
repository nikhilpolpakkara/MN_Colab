import streamlit as st
from pymongo import MongoClient
from EntryUI import TyreWear, Emission
from MongoDBOps import crud_operations

line_color = "#2a9df4"


@st.cache_resource
def load_connection():
    print("Loading Database")
    client = MongoClient("mongodb://localhost:27017/")
    return client


@st.cache_resource
def get_dept_names(_mongodb):
    dept_names = _mongodb.get_field_values_from_collection(field_name='name')
    return dept_names


# Main App
def main():
    client = load_connection()
    dept_details_handler = crud_operations.MongoDBHandler(client)
    dept_details_handler.load_database("common")
    dept_details_handler.load_collection("department_details")
    dept_names = get_dept_names(dept_details_handler)

    st.sidebar.title("TNV APP")
    st.sidebar.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)

    analytics_expander = st.sidebar.expander("ANALYTICS", expanded=True)
    entry_expander = st.sidebar.expander("DATA ENTRY", expanded=True)

    with analytics_expander:
        st.write("Analytics")

    with entry_expander:
        st.title(
            ":blue[SELECT DEPARTMENT & TEST ACTIVITY]"
        )

        selected_department = st.selectbox("Select Department".upper(), dept_names)
        st.sidebar.markdown(
            "<br>",
            unsafe_allow_html=True
        )
        activity_list = dept_details_handler.get_field_values_from_nested_array(
            collection_field_name='test_activity',
            array_field_name='name',
            filter={'name': selected_department}
        )

        selected_test_activity = st.selectbox(
            "Select Test Activity".upper(),
            activity_list
        )

        test_activity_doc = dept_details_handler.get_document_from_nested_array(
            collection_filter={'name': selected_department},
            nested_array="test_activity",
            array_document_filter={"field_name": 'name', "field_value": selected_test_activity}
        )
    test_data_handler = crud_operations.MongoDBHandler(client)
    test_data_handler.load_database(selected_department)
    test_data_handler.load_collection(selected_test_activity)

    # Display the data entry page based on the selected department and test activity
    if selected_test_activity == 'tyre_wear':
        TyreWear.test_data_entry(test_activity_doc, test_data_handler, client)
    elif selected_test_activity == 'emission':
        Emission.test_data_entry()


if __name__ == "__main__":
    main()