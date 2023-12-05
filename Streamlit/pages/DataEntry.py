import st_pages
import streamlit as st
from pymongo import MongoClient
import Mongodb_querries
from streamlit_extras.switch_page_button import switch_page
from pages import tyre_wear
from streamlit.components.v1 import html


def open_page(url):
    open_script = """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)


client = MongoClient("mongodb://localhost:27017/")
db = client["TNV"]
line_color = "#2a9df4"

department_details = db["department_details"]

entry_expander = st.expander("DATA ENTRY", expanded=True)


with entry_expander:
    st.header(
        ":blue[SELECT DEPARTMENT & TEST ACTIVITY]"
    )

    dept_names = Mongodb_querries.get_field_values_from_collection(
        collection=department_details,
        field_name='name'
    )

    selected_department = st.selectbox("Select Department".upper(), dept_names)
    st.sidebar.markdown(
        "<br>",
        unsafe_allow_html=True
    )
    activity_list = Mongodb_querries.get_field_values_from_nested_array(
        collection=department_details,
        collection_field_name='test_activity',
        array_field_name='name',
        filter={'name': selected_department}
    )

    selected_test_activity = st.selectbox(
        "Select Test Activity".upper(),
        activity_list
    )


# Display the data entry page based on the selected department and test activity
if selected_test_activity == 'tyre_wear':
    # switch_page('tyre_wear')
    # st_pages.Page('pages/tyre_wear.py')
    # st.link_button("DONE", url="http://localhost:8501/tyre_wear")
    # tyre_wear.tyre_wear_entry()
    st.button('Open link', on_click=open_page, args=(f'https://localhost:8501/#{selected_test_activity}',))
# elif selected_test_activity == 'emission':
#     # emission_page(selected_department, selected_test_activity, department_details)
#     st.link_button("DONE", url="http://localhost:8501/tyre_wear")