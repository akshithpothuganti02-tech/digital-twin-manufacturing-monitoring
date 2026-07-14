from collections import defaultdict
from typing import Any


# Stores the latest processed state of every machine.
#
# Example:
# {
#     "M001": {
#         "machine_id": "M001",
#         "temperature": 50.2,
#         "health_score": 100,
#         "status": "Healthy"
#     }
# }
digital_twin: dict[str, dict[str, Any]] = {}


# Stores warning and critical alert records.
alerts: list[dict[str, Any]] = []


# Stores recent historical readings for every machine.
#
# Example:
# {
#     "M001": [
#         {...reading 1...},
#         {...reading 2...}
#     ]
# }
history: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)


# Maximum number of historical records retained for each machine.
MAX_HISTORY_RECORDS = 50


def update_machine(machine) -> None:
    """
    Save the latest sensor snapshot and add it to machine history.

    The machine argument is a Pydantic MachineState object.
    """

    # Convert the Pydantic model into a regular Python dictionary.
    data = machine.model_dump()

    # Save the latest state for the selected machine.
    digital_twin[machine.machine_id] = data.copy()

    # Add a separate copy to history.
    #
    # Using copy() prevents later updates to digital_twin from
    # accidentally changing previous historical records.
    history[machine.machine_id].append(data.copy())

    # Keep only the latest configured number of records.
    if len(history[machine.machine_id]) > MAX_HISTORY_RECORDS:
        history[machine.machine_id].pop(0)


def update_health(
    machine_id: str,
    score: int,
    status: str
) -> None:
    """
    Add the calculated health score and status to the latest
    Digital Twin state and historical record.
    """

    if machine_id not in digital_twin:
        raise KeyError(
            f"Cannot update health because machine '{machine_id}' "
            "does not exist in the Digital Twin."
        )

    digital_twin[machine_id]["health_score"] = score
    digital_twin[machine_id]["status"] = status

    # Update the most recent historical record.
    if history[machine_id]:
        history[machine_id][-1]["health_score"] = score
        history[machine_id][-1]["status"] = status


def update_prediction(
    machine_id: str,
    prediction: dict[str, Any]
) -> None:
    """
    Add predictive-maintenance information to the machine's
    latest Digital Twin state and most recent historical record.

    Expected prediction format:

    {
        "prediction": "Possible bearing wear",
        "severity": "High",
        "recommendation": "Inspect the bearings.",
        "detected_conditions": [...]
    }
    """

    if machine_id not in digital_twin:
        raise KeyError(
            f"Cannot update prediction because machine '{machine_id}' "
            "does not exist in the Digital Twin."
        )

    predicted_fault = prediction.get(
        "prediction",
        "Prediction unavailable"
    )

    severity = prediction.get(
        "severity",
        "Unknown"
    )

    recommendation = prediction.get(
        "recommendation",
        "No recommendation available"
    )

    digital_twin[machine_id]["prediction"] = predicted_fault
    digital_twin[machine_id]["prediction_severity"] = severity
    digital_twin[machine_id]["recommendation"] = recommendation

    # A machine can satisfy multiple predictive rules.
    # Store the complete list when it is available.
    detected_conditions = prediction.get("detected_conditions")

    if detected_conditions is not None:
        digital_twin[machine_id][
            "detected_conditions"
        ] = detected_conditions
    else:
        # Remove old detected conditions when the machine returns
        # to normal operation.
        digital_twin[machine_id].pop(
            "detected_conditions",
            None
        )

    # Update the latest historical record as well.
    if history[machine_id]:
        latest_record = history[machine_id][-1]

        latest_record["prediction"] = predicted_fault
        latest_record["prediction_severity"] = severity
        latest_record["recommendation"] = recommendation

        if detected_conditions is not None:
            latest_record[
                "detected_conditions"
            ] = detected_conditions
        else:
            latest_record.pop(
                "detected_conditions",
                None
            )


def add_alert(alert: dict[str, Any]) -> None:
    """
    Add an alert to the in-memory alert collection.
    """

    alerts.append(alert.copy())

    # Prevent unlimited memory growth.
    if len(alerts) > 200:
        alerts.pop(0)


def get_alerts() -> list[dict[str, Any]]:
    """
    Return all stored alerts.
    """

    return alerts


def get_all_machines() -> dict[str, dict[str, Any]]:
    """
    Return the latest state of all machines.
    """

    return digital_twin


def get_machine(machine_id: str) -> dict[str, Any] | None:
    """
    Return the latest state of one machine.
    """

    return digital_twin.get(machine_id)


def get_machine_history(
    machine_id: str
) -> list[dict[str, Any]]:
    """
    Return recent historical records for one machine.
    """

    return history[machine_id]