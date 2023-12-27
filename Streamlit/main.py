import streamlit as st
from pymongo import MongoClient
from EntryUI import TyreWear, TyreWear2, Emission, TestTimeline
from DBOps import crud_operations
from streamlit_tree_select import tree_select

line_color = "#2a9df4"


@st.cache_resource(ttl="30s")
def load_connection():
    print("Establishing Database Connection")
    # client = MongoClient("mongodb://localhost:27017/")
    # client = MongoClient("mongodb://10.11.10.95:27017/")
    client = MongoClient("mongodb://10.11.10.72:27017/")
    # client = MongoClient("mongodb+srv://nikhilpolpakkara:Aspire_13@cluster0.4cun9lz.mongodb.net/?retryWrites=true&w=majority")
    return client


@st.cache_resource(ttl="30s")
def load_data_handler(database, collection, _client):
    print("Loading Data Handler")
    dept_details_handler = crud_operations.MongoDBHandler(_client)
    dept_details_handler.load_database("common")
    dept_details_handler.load_collection("department_details")
    return dept_details_handler


@st.cache_resource
def get_dept_names(_mongodb):
    print("getting dept names")
    dept_names = _mongodb.get_field_values_from_level_1_collection(field_names=['name'])
    return dept_names


@st.cache_resource
def get_activity_list(_dept_details_handler, selected_department):
    print("Getting Activity List")
    activity_list = _dept_details_handler.get_field_values_from_level_2_collection(
        collection_field_name='test_activity',
        array_field_name='name',
        collection_filter={'name': selected_department}
    )
    return activity_list


# @st.cache_resource(experimental_allow_widgets=True)
def load_entry_page(selected_department, selected_test_activity, _client):
    print("Loading Entry Page")
    if selected_test_activity == "tyre_wear":
        TyreWear2.test_data_entry(
            department_name=selected_department,
            test_activity_name=selected_test_activity,
            client=_client
        )
    elif selected_test_activity == "emission":
        Emission.emission_entry()


def load_analytics_page(selected_department, selected_analytics, _client):
    if selected_analytics == "tyre wear analytics":
        TyreWear2.tyre_wear_analytics(selected_department, _client)



def load_dashboard_page(selected_dashboard, _client):
    if selected_dashboard == "test_timeline":
        TestTimeline.plotly_timeline(_client)


def update_entry_sidebar(selected_department, _sidebar):
    print("Loading Department Specific Sidebar")

    if selected_department == "durability":
        vehicle_entry_page = False
        with _sidebar:
            if st.button("ADD NEW VEHICLE"):
                vehicle_entry_page = True
        if vehicle_entry_page is True:
            TyreWear2.add_new_vehicle()


def create_expander_dict():
    expander_dict = {
        "analytics_expander": st.sidebar.expander("ANALYTICS", expanded=True),
        "test_entry_expander": st.sidebar.expander("TEST DATA ENTRY"),
        "vehicle_entry_expander": st.sidebar.expander("NEW COMPONENT/VEHICLE ENTRY"),
        "dashboards_expander": st.sidebar.expander("DASHBOARDS")
    }
    return expander_dict


# Main App
def main():
    print("----------------Starting app----------------")

    print("loading sidebar")
    st.sidebar.title("TNV APP")
    st.sidebar.markdown(f'<hr style="border-top: 1px solid {line_color};">', unsafe_allow_html=True)
    client = load_connection()

    # mode = st.sidebar.selectbox("WHAT YOU WANT TO DO ?", ["TEST DATA ENTRY", "ADD NEW VEHICLE/COMPONENT", "ANALYTICS", "DASHBOARDS"])
    # dept_details_handler = load_data_handler(
    #     database="common",
    #     collection="department_details",
    #     _client=client
    # )
    # dept_names = get_dept_names(dept_details_handler)
    #
    # if mode == "ANALYTICS":
    #     selected_department = st.sidebar.selectbox("Department".upper(), dept_names, index=None)
    #     expander_dict = create_expander_dict()
    #     print("Loading sidebar expanders")
    #     with expander_dict["analytics_expander"]:
    #         selected_analytics = st.selectbox("SELECT ANALYTICS",
    #                                           dept_details_handler.get_field_values_from_level_1_document(
    #                                               l_1_c_filter={"name": selected_department},
    #                                               l_1_d_field_name="analytics"
    #                                           ),
    #                                           index=None
    #                                           )
    #     load_analytics_page(selected_department, selected_analytics, client)
    # elif mode == "TEST DATA ENTRY":
    #     selected_department = st.sidebar.selectbox("Department".upper(), dept_names, index=None)
    #     expander_dict = create_expander_dict()
    #
    #     with expander_dict["test_entry_expander"]:
    #         st.sidebar.markdown(
    #             "<br>",
    #             unsafe_allow_html=True
    #         )
    #         activity_list = get_activity_list(dept_details_handler, selected_department)
    #
    #         selected_test_activity = st.selectbox(
    #             "Select Test Activity".upper(),
    #             activity_list,
    #             index=None
    #         )
    #
    #     load_entry_page(selected_department, selected_test_activity, client)
    #     # update_entry_sidebar(selected_department, expander_dict["entry_expander"])

    nodes = [
        {
            "label": "TNV",
            "value": "tnv",
            "children": [
                {
                    "label": "TEST TIMELINE",
                    "value": "test_timeline"
                }
            ]
        },


        {
            "label": "DURABILITY",
            "value": "durability",
            "children": [
                {
                    "label": "DASHBOARDS",
                    "value": "durability_dashboard",
                    "children": [
                        {
                            "label": "DASHBOARD 1",
                            "value": "dashboard_1"
                        }
                    ]

                },

                {
                    "label": "ANALYTICS",
                    "value": "durability_analytics",
                    "children": [
                        {
                            "label": "TYRE WEAR ANALYSIS",
                            "value": "tyre_wear_analysis"
                        }
                    ]
                },
                {
                    "label": "DATA ENTRY",
                    "value": "durability_data_entry",
                    "children": [
                        {
                            "label": "TYRE WEAR ENTRY",
                            "value": "entry_tyre_wear"
                        }
                    ]
                },
            ],
        },

        {
            "label": "CALIBRATION",
            "value": "cal",
            "children": [
                {
                    "label": "DASHBOARD",
                    "value": "cal_dashboard",
                    "children": [
                        {
                            "label": "2W EMISSION DASHBOARD",
                            "value": "emission_dashboard_2w"
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
            ],
        }
    ]
    with st.sidebar:
        tree = tree_select(nodes, only_leaf_checkboxes=True)

    checkbox_ticked = list(set(tree["checked"]) - set(tree["expanded"]))
    print(checkbox_ticked)
    if len(checkbox_ticked) == 0:
        # st.error("Please select something")
        st.image(image="data/main_gif_2.gif",
                 use_column_width=True,
                 caption = "WELCOME"
                )

    else:
        if len(checkbox_ticked) > 1:
            st.error("Please select only one option in sidebar")
        else:
            selected_page = checkbox_ticked[0]
            print(selected_page)
            if selected_page == "entry_tyre_wear":
                load_entry_page("durability", "tyre_wear", client)
            elif selected_page == "tyre_wear_analysis":
                load_analytics_page("durability", "tyre wear analytics", client)
            elif selected_page == "test_timeline":
                load_dashboard_page(selected_page, client)
            elif selected_page == "emission_analysis":
                Emission.emission_analysis_ui()
            elif selected_page == "emission_dashboard_2w":
                # client.close()
                Emission.emission_dashboard_2w()


if __name__ == "__main__":
    main()