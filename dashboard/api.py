import requests

from config import FOG_NODE_URL


def get_machines():

    response = requests.get(
        f"{FOG_NODE_URL}/machines",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def get_alerts():

    response = requests.get(
        f"{FOG_NODE_URL}/alerts",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def get_machine_history(machine_id):

    response = requests.get(
        f"{FOG_NODE_URL}/history/{machine_id}",
        timeout=5
    )

    response.raise_for_status()

    return response.json()