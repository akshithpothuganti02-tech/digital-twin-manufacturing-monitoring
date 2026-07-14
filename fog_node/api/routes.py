from fastapi import APIRouter
import requests

from fog_node.models.machine_state import MachineState

from fog_node.processors.predictive_maintenance import predict_failure

from fog_node.processors.health_processor import (
    calculate_health,
    get_health_status
)

from fog_node.services.twin_service import (
    update_machine,
    update_health,
    update_prediction,
    add_alert,
    get_all_machines,
    get_machine,
    get_alerts,
    get_machine_history
)

router = APIRouter()


# API Gateway URL
API_GATEWAY_URL = (
    "https://qp5je0pxx2.execute-api.us-east-1.amazonaws.com/telemetry"
)


@router.post("/machine-data")
def receive_machine_data(machine: MachineState):

    # Update latest machine values
    update_machine(machine)

    # Calculate health
    score = calculate_health(machine)
    status = get_health_status(score)

    update_health(
        machine.machine_id,
        score,
        status
    )

    # Predictive maintenance
    prediction = predict_failure(machine)

    update_prediction(
        machine.machine_id,
        prediction
    )

    # Add alert if required
    if status != "Healthy":
        add_alert({
            "machine_id": machine.machine_id,
            "machine_name": machine.machine_name,
            "health_score": score,
            "status": status,
            "timestamp": machine.timestamp
        })

    # -----------------------------
    # Upload telemetry to AWS Cloud
    # -----------------------------
    try:

        cloud_payload = get_machine(machine.machine_id)

        response = requests.post(
            API_GATEWAY_URL,
            json=cloud_payload,
            timeout=5
        )

        print(
            f"Cloud upload successful: "
            f"{response.status_code}"
        )

    except Exception as error:

        print(
            f"Cloud upload failed: {error}"
        )

    return {
        "message": "Machine processed",
        "machine_id": machine.machine_id,
        "health_score": score,
        "status": status,
        "prediction": prediction
    }


@router.get("/machines")
def all_machines():

    return get_all_machines()


@router.get("/machines/{machine_id}")
def single_machine(machine_id: str):

    machine = get_machine(machine_id)

    if machine is None:
        return {
            "message": "Machine not found"
        }

    return machine


@router.get("/alerts")
def all_alerts():

    return get_alerts()


@router.get("/history/{machine_id}")
def machine_history(machine_id: str):

    return get_machine_history(machine_id)