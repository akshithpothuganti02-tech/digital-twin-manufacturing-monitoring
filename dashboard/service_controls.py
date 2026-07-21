import subprocess
import time

import streamlit as st


SERVICES = {
    "fog": {
        "label": "Fog Node",
        "service": "digital-twin-fog.service",
    },
    "simulator": {
        "label": "Sensor Simulator",
        "service": "digital-twin-simulator.service",
    },
    "dashboard": {
        "label": "Dashboard",
        "service": "digital-twin-dashboard.service",
    },
}


def run_systemctl(action: str, service: str) -> tuple[bool, str]:
    allowed_actions = {"start", "stop", "restart", "is-active"}

    if action not in allowed_actions:
        return False, "Unsupported service action."

    try:
        result = subprocess.run(
            ["sudo", "/usr/bin/systemctl", action, service],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )

        output = (result.stdout or result.stderr).strip()
        return result.returncode == 0, output

    except subprocess.TimeoutExpired:
        return False, "The service command timed out."

    except Exception as error:
        return False, str(error)


def service_is_active(service: str) -> bool:
    success, output = run_systemctl("is-active", service)
    return success and output == "active"


def render_service_controls() -> None:
    st.subheader("⚙️ System Controls")
    st.caption("Start, stop, or restart the Digital Twin services.")

    fog_active = service_is_active(SERVICES["fog"]["service"])
    simulator_active = service_is_active(SERVICES["simulator"]["service"])
    dashboard_active = service_is_active(SERVICES["dashboard"]["service"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Fog Node")
        st.success("● Running") if fog_active else st.error("● Stopped")

        start_col, stop_col = st.columns(2)

        with start_col:
            if st.button(
                "▶ Start Fog",
                disabled=fog_active,
                use_container_width=True,
            ):
                success, message = run_systemctl(
                    "start",
                    SERVICES["fog"]["service"],
                )
                if success:
                    st.success("Fog Node started.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Could not start Fog Node: {message}")

        with stop_col:
            if st.button(
                "⏹ Stop Fog",
                disabled=not fog_active,
                use_container_width=True,
            ):
                success, message = run_systemctl(
                    "stop",
                    SERVICES["fog"]["service"],
                )
                if success:
                    st.warning("Fog Node stopped.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Could not stop Fog Node: {message}")

    with col2:
        st.markdown("### Simulator")
        st.success("● Running") if simulator_active else st.error("● Stopped")

        start_col, stop_col = st.columns(2)

        with start_col:
            if st.button(
                "▶ Start Simulator",
                disabled=simulator_active,
                use_container_width=True,
            ):
                success, message = run_systemctl(
                    "start",
                    SERVICES["simulator"]["service"],
                )
                if success:
                    st.success("Simulator started.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Could not start Simulator: {message}")

        with stop_col:
            if st.button(
                "⏹ Stop Simulator",
                disabled=not simulator_active,
                use_container_width=True,
            ):
                success, message = run_systemctl(
                    "stop",
                    SERVICES["simulator"]["service"],
                )
                if success:
                    st.warning("Simulator stopped.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Could not stop Simulator: {message}")

    with col3:
        st.markdown("### Dashboard")
        st.success("● Running") if dashboard_active else st.error("● Stopped")

        if st.button(
            "🔄 Restart Dashboard",
            use_container_width=True,
        ):
            st.warning("Dashboard is restarting. Refresh after a few seconds.")
            run_systemctl(
                "restart",
                SERVICES["dashboard"]["service"],
            )

        if st.button(
            "⏹ Stop Dashboard",
            use_container_width=True,
        ):
            st.warning(
                "Dashboard is stopping. Restart it through SSH with:\n\n"
                "`sudo systemctl start digital-twin-dashboard`"
            )
            time.sleep(2)
            run_systemctl(
                "stop",
                SERVICES["dashboard"]["service"],
            )

    st.divider()
