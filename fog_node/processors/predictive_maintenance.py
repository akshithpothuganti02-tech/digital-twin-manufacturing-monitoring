
def predict_failure(machine):
    detected_conditions = []

    if machine.temperature > 80 and machine.vibration > 1.5:
        detected_conditions.append({
            "fault": "Possible bearing wear",
            "severity": "High",
            "recommendation": (
                "Inspect and lubricate the bearings during "
                "the next maintenance window."
            ),
        })

    if machine.power > 6 and machine.rpm < 1000:
        detected_conditions.append({
            "fault": "Possible motor overload",
            "severity": "High",
            "recommendation": (
                "Inspect the motor load, electrical supply, "
                "and cooling system."
            ),
        })

    if machine.pressure > 120:
        detected_conditions.append({
            "fault": "Possible pressure-system blockage",
            "severity": "Medium",
            "recommendation": (
                "Inspect pressure lines, valves, and filters."
            ),
        })

    if machine.vibration > 2:
        detected_conditions.append({
            "fault": "Possible shaft misalignment",
            "severity": "High",
            "recommendation": (
                "Inspect shaft alignment and rotating components."
            ),
        })

    if machine.temperature > 85 and machine.power > 5:
        detected_conditions.append({
            "fault": "Possible cooling-system degradation",
            "severity": "High",
            "recommendation": (
                "Inspect cooling fans, ventilation, "
                "and coolant circulation."
            ),
        })

    if not detected_conditions:
        return {
            "prediction": "No immediate failure predicted",
            "severity": "Normal",
            "recommendation": (
                "Continue normal operation and routine monitoring."
            ),
        }

    # Choose the highest severity fault
    severity_priority = {
        "Normal": 0,
        "Low": 1,
        "Medium": 2,
        "High": 3,
    }

    primary_fault = max(
        detected_conditions,
        key=lambda condition: severity_priority.get(
            condition["severity"],
            0,
        ),
    )

    return {
        "prediction": primary_fault["fault"],
        "severity": primary_fault["severity"],
        "recommendation": primary_fault["recommendation"],
        "detected_conditions": detected_conditions,
    }