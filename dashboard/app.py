import streamlit as st

from machine_details import render_machine_details
from config import PAGE_TITLE
from config import PAGE_ICON
from config import LAYOUT

from api import get_machines
from api import get_alerts

from sidebar import render_sidebar
from metrics import render_metrics
from machine_table import render_machine_table
from alerts import render_alerts
from api import get_machine_history

from charts import (
    render_temperature_chart,
    render_rpm_chart,
    render_power_chart,
    render_status_pie
)



st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)



st.title("🏭 Digital Twin Manufacturing Monitoring")



render_sidebar()



machines = get_machines()

alerts = get_alerts()


render_metrics(machines)
st.divider()

st.subheader("📊 Machine Analytics")

machine_ids = list(machines.keys())


selected_machine = st.selectbox(
    "Select Machine",
    machine_ids,
    format_func=lambda machine_id: (
        f"{machine_id} - {machines[machine_id]['machine_name']}"
    )
)
history = get_machine_history(selected_machine)
selected_machine_data = machines[selected_machine]

render_machine_details(selected_machine_data)

st.divider()

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


render_machine_table(machines)

st.divider()


render_alerts(alerts)