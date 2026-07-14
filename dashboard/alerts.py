import pandas as pd

import streamlit as st


def render_alerts(alerts):

    st.subheader("🚨 Alerts")

    if alerts:

        st.dataframe(
            pd.DataFrame(alerts),
            width="stretch",
            hide_index=True
        )

    else:

        st.success("No Alerts")