import time
import requests

from config.settings import MACHINES, DISPATCH_INTERVAL_SECONDS
from sensors.machine import Machine
from sensors.generator import generate_machine_snapshot

# Fog Node endpoint
FOG_NODE_URL = "http://127.0.0.1:8000/machine-data"


def create_machines():
    machines = []

    for machine_config in MACHINES:
        machine = Machine(
            machine_id=machine_config["machine_id"],
            machine_name=machine_config["machine_name"]
        )
        machines.append(machine)

    return machines


def send_to_fog_node(snapshot):
    """
    Send machine snapshot to the Fog Node.
    """

    try:
        response = requests.post(
            FOG_NODE_URL,
            json=snapshot,
            timeout=5
        )

        if response.status_code == 200:
            print(f"✅ Sent {snapshot['machine_id']} to Fog Node")
        else:
            print(f"❌ Error {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Fog Node is not running")

    except Exception as error:
        print(error)


def run_simulator():

    machines = create_machines()

    print("=" * 50)
    print("Digital Twin Manufacturing Sensor Simulator")
    print("=" * 50)

    while True:

        for machine in machines:

            snapshot = generate_machine_snapshot(machine)

            print(snapshot)

            send_to_fog_node(snapshot)

        print("-" * 50)

        time.sleep(DISPATCH_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_simulator()