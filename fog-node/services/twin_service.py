import pandas as pd
import requests
import streamlit as st
import time

FOG_NODE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Digital Twin Dashboard",
    layout="wide"
)

st.title("🏭 Digital Twin Manufacturing Monitoring")

try:
    machines = requests.get(f"{FOG_NODE}/machines", timeout=5).json()
    alerts = requests.get(f"{FOG_NODE}/alerts", timeout=5).json()

    st.header("Machine Status")

    if machines:
        rows = []

        for machine in machines.values():
            rows.append({
                "Machine": machine["machine_name"],
                "Temperature": machine["temperature"],
                "Vibration": machine["vibration"],
                "Power": machine["power"],
                "RPM": machine["rpm"],
                "Pressure": machine["pressure"],
                "Health Score": machine["health_score"],
                "Status": machine["status"]
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.warning("No machine data available yet.")

    st.divider()

    st.header("Alerts")

    if alerts:
        st.dataframe(pd.DataFrame(alerts), use_container_width=True)
    else:
        st.success("No alerts detected.")

except Exception as e:
    st.error(f"Dashboard error: {e}")

time.sleep(3)
st.rerun()