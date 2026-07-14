DISPATCH_INTERVAL_SECONDS = 5

MACHINES = [
    {
        "machine_id": "M001",
        "machine_name": "Conveyor Belt"
    },
    {
        "machine_id": "M002",
        "machine_name": "Robotic Arm"
    },
    {
        "machine_id": "M003",
        "machine_name": "Drilling Machine"
    },
    {
        "machine_id": "M004",
        "machine_name": "Cooling Unit"
    },
    {
        "machine_id": "M005",
        "machine_name": "Packaging Machine"
    }
]

SENSOR_TYPES = {
    "temperature": {
        "min": 35,
        "max": 95,
        "unit": "C"
    },
    "vibration": {
        "min": 0.1,
        "max": 3.5,
        "unit": "mm/s"
    },
    "power": {
        "min": 1.0,
        "max": 8.0,
        "unit": "kW"
    },
    "rpm": {
        "min": 400,
        "max": 1800,
        "unit": "RPM"
    },
    "pressure": {
        "min": 60,
        "max": 140,
        "unit": "PSI"
    }
}