import random
from config.machine_profiles import MACHINE_PROFILES


class Machine:

    def __init__(self, machine_id, machine_name):

        self.machine_id = machine_id
        self.machine_name = machine_name

        profile = MACHINE_PROFILES[machine_name]

        # Initial sensor values
        self.temperature = random.uniform(*profile["temperature"])
        self.vibration = random.uniform(*profile["vibration"])
        self.power = random.uniform(*profile["power"])
        self.rpm = random.uniform(*profile["rpm"])
        self.pressure = random.uniform(*profile["pressure"])

    def to_dict(self):

        return {

            "machine_id": self.machine_id,

            "machine_name": self.machine_name,

            "temperature": round(self.temperature, 2),

            "vibration": round(self.vibration, 2),

            "power": round(self.power, 2),

            "rpm": round(self.rpm, 2),

            "pressure": round(self.pressure, 2)

        }