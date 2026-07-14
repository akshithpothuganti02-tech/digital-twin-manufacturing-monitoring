import random

from utils.helpers import get_current_timestamp


def update_sensor(current_value, minimum, maximum, change):

    current_value += random.uniform(-change, change)

    current_value = max(minimum, min(maximum, current_value))

    return current_value


def generate_machine_snapshot(machine):

    machine.temperature = update_sensor(
        machine.temperature,
        20,
        95,
        1
    )

    machine.vibration = update_sensor(
        machine.vibration,
        0.1,
        3,
        0.05
    )

    machine.power = update_sensor(
        machine.power,
        1,
        8,
        0.2
    )

    machine.rpm = update_sensor(
        machine.rpm,
        700,
        1600,
        20
    )

    machine.pressure = update_sensor(
        machine.pressure,
        60,
        130,
        2
    )

    snapshot = machine.to_dict()

    snapshot["timestamp"] = get_current_timestamp()

    return snapshot