import streamlit as st


def render_machine_details(machine: dict) -> None:
    st.subheader("🔍 Selected Machine Digital Twin")

    machine_name = machine.get("machine_name", "Unknown")
    status = machine.get("status", "Unknown")
    health_score = machine.get("health_score", 0)

    status_icons = {
        "Healthy": "🟢 Healthy",
        "Warning": "🟡 Warning",
        "Critical": "🔴 Critical",
    }

    st.markdown(f"### {machine_name}")
    st.write(f"**Status:** {status_icons.get(status, status)}")

    row1_col1, row1_col2, row1_col3 = st.columns(3)

    row1_col1.metric(
        "Health Score",
        f"{health_score}%"
    )

    row1_col2.metric(
        "Temperature",
        f"{machine.get('temperature', 0)} °C"
    )

    row1_col3.metric(
        "Vibration",
        f"{machine.get('vibration', 0)} mm/s"
    )

    row2_col1, row2_col2, row2_col3 = st.columns(3)

    row2_col1.metric(
        "Power",
        f"{machine.get('power', 0)} kW"
    )

    row2_col2.metric(
        "RPM",
        machine.get("rpm", 0)
    )

    row2_col3.metric(
        "Pressure",
        f"{machine.get('pressure', 0)} PSI"
    )

    st.subheader("🔮 Predictive Maintenance")

    prediction = machine.get(
        "prediction",
        "Prediction unavailable"
    )

    severity = machine.get(
        "prediction_severity",
        "Unknown"
    )

    recommendation = machine.get(
        "recommendation",
        "No recommendation available"
    )

    prediction_message = (
        f"**Predicted condition:** {prediction}\n\n"
        f"**Severity:** {severity}\n\n"
        f"**Recommendation:** {recommendation}"
    )

    if severity == "High":
        st.error(prediction_message)

    elif severity == "Medium":
        st.warning(prediction_message)

    else:
        st.success(prediction_message)

    detected_conditions = machine.get(
        "detected_conditions",
        []
    )

    if detected_conditions:
        with st.expander("View all detected conditions"):
            for condition in detected_conditions:
                st.markdown(
                    f"""
**Fault:** {condition.get("fault", "Unknown")}  
**Severity:** {condition.get("severity", "Unknown")}  
**Recommendation:** {condition.get("recommendation", "Not available")}
"""
                )
                st.divider()