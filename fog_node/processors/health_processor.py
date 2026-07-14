

def calculate_health(machine):

    score = 100

    # Temperature
    if machine.temperature > 85:
        score -= 20

    # Vibration
    if machine.vibration > 2.0:
        score -= 20

    # Power
    if machine.power > 6:
        score -= 15

    # Pressure
    if machine.pressure > 120:
        score -= 15

    # RPM
    if machine.rpm < 900:
        score -= 10

    return max(score, 0)
def get_health_status(score):

    if score >= 90:
        return "Healthy"

    if score >= 70:
        return "Warning"

    return "Critical"