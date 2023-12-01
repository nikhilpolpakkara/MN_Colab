import streamlit as st


def main():
    st.title("HOME")

    # Include Bootstrap CSS
    st.markdown(
        '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" '
        'integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" '
        'crossorigin="anonymous">'
        , unsafe_allow_html=True
    )

    # Bootstrap container
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # Bootstrap row
    st.markdown('<div class="row">', unsafe_allow_html=True)

    # Card 1 with a blue background
    st.markdown('<div class="col-md-6">', unsafe_allow_html=True)
    st.markdown('<div class="card bg-primary text-white">', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)
    st.header("ANALYTICS")
    st.write("For Dashboards and Analytics")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 2 with a green background
    st.markdown('<div class="col-md-6">', unsafe_allow_html=True)
    st.markdown('<div class="card bg-success text-white">', unsafe_allow_html=True)
    st.markdown('<div class="card-body">', unsafe_allow_html=True)
    st.header("DATA ENTRY")
    st.write("For Test Data Entry")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Close Bootstrap row and container
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
