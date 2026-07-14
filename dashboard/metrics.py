import streamlit as st


def render_metrics(machines):

    healthy = 0
    warning = 0
    critical = 0

    for machine in machines.values():

        status = machine["status"]

        if status == "Healthy":
            healthy += 1

        elif status == "Warning":
            warning += 1

        else:
            critical += 1

    total = len(machines)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "⚙️ Total",
        total
    )

    col2.metric(
        "🟢 Healthy",
        healthy
    )

    col3.metric(
        "🟡 Warning",
        warning
    )

    col4.metric(
        "🔴 Critical",
        critical
    )