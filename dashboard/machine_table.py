import pandas as pd

import streamlit as st


def render_machine_table(machines):

    rows = []

    for machine in machines.values():

        rows.append({

            "Machine":
            machine["machine_name"],

            "Temperature":
            machine["temperature"],

            "Power":
            machine["power"],

            "RPM":
            machine["rpm"],

            "Pressure":
            machine["pressure"],

            "Health":
            machine["health_score"],

            "Status":
            machine["status"]

        })

    st.subheader("🏭 Live Machine Status")

    st.dataframe(
        pd.DataFrame(rows),
        width="stretch",
        hide_index=True
    )