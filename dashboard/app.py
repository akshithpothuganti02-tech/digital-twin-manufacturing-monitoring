import streamlit as st

from alerts import render_alerts
from api import (
    get_alerts,
    get_machine_history,
    get_machines,
)
from charts import (
    render_power_chart,
    render_rpm_chart,
    render_status_pie,
    render_temperature_chart,
)
from config import LAYOUT, PAGE_ICON, PAGE_TITLE
from machine_details import render_machine_details
from machine_table import render_machine_table
from metrics import render_metrics
from sidebar import render_sidebar
from service_controls import render_service_controls

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
)


st.title("🏭 Digital Twin Manufacturing Monitoring")

render_sidebar()
render_service_controls()	

# --------------------------------------------------
# Load data from the Fog Node
# --------------------------------------------------
try:
    machines = get_machines()
except Exception as error:
    st.error(
        "Could not load machine data from the Fog Node.\n\n"
        f"Error: {error}"
    )
    st.stop()


try:
    alerts = get_alerts()
except Exception as error:
    st.warning(
        "Could not load alert data.\n\n"
        f"Error: {error}"
    )
    alerts = []


if not machines:
    st.warning(
        "No machine data is available yet. "
        "Start the Fog Node and sensor simulator, then refresh this page."
    )
    st.stop()


# --------------------------------------------------
# System Status Dashboard
# --------------------------------------------------

active_alerts = [
    alert
    for alert in alerts
    if alert.get("active", True)
]

running_count = sum(
    1
    for machine in machines.values()
    if machine.get("operational_status", "Running") == "Running"
)

total_count = len(machines)

critical_alerts = [
    alert
    for alert in active_alerts
    if alert.get("status") in ["Critical", "Offline"]
]

warning_alerts = [
    alert
    for alert in active_alerts
    if alert.get("status") == "Warning"
]


# --------------------------------------------------
# Green Banner
# --------------------------------------------------

if not critical_alerts and not warning_alerts:

    st.success(
        f"""
## 🟢 System Status

**Running Machines:** {running_count}/{total_count}

✅ No active critical alerts.

All machines are operating normally.
"""
    )


# --------------------------------------------------
# Yellow Banner
# --------------------------------------------------

elif warning_alerts and not critical_alerts:

    latest = warning_alerts[-1]

    st.warning(
        f"""
## ⚠️ SYSTEM WARNING

**Running Machines:** {running_count}/{total_count}

Machine:
{latest.get("machine_id")} - {latest.get("machine_name")}

Condition:
{latest.get("prediction", "Warning detected")}

Recommendation:
{latest.get("recommendation", "Inspect machine")}
"""
    )


# --------------------------------------------------
# Red Banner
# --------------------------------------------------

else:

    latest = critical_alerts[-1]

    st.error(
        f"""
# 🚨 CRITICAL MACHINE ALERT 🚨

**Running Machines:** {running_count}/{total_count}

Machine:
{latest.get("machine_id")} - {latest.get("machine_name")}

Status:
{latest.get("status")}

Health Score:
{latest.get("health_score")}

Condition:
{latest.get("prediction", "Critical condition")}

Recommendation:
{latest.get("recommendation", "Immediate action required")}
"""
    )

# --------------------------------------------------
# Overview metrics
# --------------------------------------------------
render_metrics(machines)

st.divider()


# --------------------------------------------------
# Machine analytics and control
# --------------------------------------------------
st.subheader("📊 Machine Analytics")

machine_ids = list(machines.keys())

selected_machine = st.selectbox(
    "Select Machine",
    machine_ids,
    format_func=lambda machine_id: (
        f"{machine_id} - "
        f"{machines[machine_id].get('machine_name', 'Unknown Machine')}"
    ),
)


try:
    history = get_machine_history(selected_machine)
except Exception as error:
    st.warning(
        "Could not load machine history.\n\n"
        f"Error: {error}"
    )
    history = []


selected_machine_data = machines.get(selected_machine)

if selected_machine_data:
    render_machine_details(selected_machine_data)
else:
    st.error("Selected machine data is unavailable.")


st.divider()


# --------------------------------------------------
# Charts
# --------------------------------------------------
left, right = st.columns(2)

with left:
    render_temperature_chart(history)

with right:
    render_status_pie(machines)


left, right = st.columns(2)

with left:
    render_power_chart(history)

with right:
    render_rpm_chart(history)


st.divider()


# --------------------------------------------------
# Machine table
# --------------------------------------------------
render_machine_table(machines)


st.divider()


# --------------------------------------------------
# Active alerts
# --------------------------------------------------
st.subheader("🚨 Active Alerts")

if active_alerts:
    render_alerts(active_alerts)
else:
    st.success("✅ No active machine alerts.")


# --------------------------------------------------
# Resolved alert history
# --------------------------------------------------
resolved_alerts = [
    alert
    for alert in alerts
    if alert.get("resolved", False)
]

if resolved_alerts:
    with st.expander("View resolved alert history"):
        render_alerts(resolved_alerts)
