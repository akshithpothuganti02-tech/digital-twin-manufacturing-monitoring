import pandas as pd
import plotly.express as px
import streamlit as st


def render_temperature_chart(history):

    if not history:
        return

    df = pd.DataFrame(history)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(
        df,
        x="timestamp",
        y="temperature",
        title="🌡 Temperature Trend",
        markers=True
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        width="stretch"
    )


def render_rpm_chart(history):

    if not history:
        return

    df = pd.DataFrame(history)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(
        df,
        x="timestamp",
        y="rpm",
        title="⚙ RPM Trend",
        markers=True
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        width="stretch"
    )


def render_power_chart(history):

    if not history:
        return

    df = pd.DataFrame(history)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(
        df,
        x="timestamp",
        y="power",
        title="⚡ Power Consumption",
        markers=True
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        width="stretch"
    )


def render_status_pie(machines):

    status = {
        "Healthy": 0,
        "Warning": 0,
        "Critical": 0
    }

    for machine in machines.values():
        status[machine["status"]] += 1

    fig = px.pie(
        values=status.values(),
        names=status.keys(),
        title="Machine Status Distribution"
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        width="stretch"
    )