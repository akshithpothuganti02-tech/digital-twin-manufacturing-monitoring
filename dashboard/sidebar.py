import streamlit as st


def render_sidebar():

    st.sidebar.title("🏭 System")

    st.sidebar.success("Online")

    st.sidebar.write("✔ Sensor Simulator")

    st.sidebar.write("✔ Fog Node")

    st.sidebar.write("✔ Dashboard")

    st.sidebar.divider()

    st.sidebar.info(
        "Digital Twin Manufacturing Monitoring"
    )