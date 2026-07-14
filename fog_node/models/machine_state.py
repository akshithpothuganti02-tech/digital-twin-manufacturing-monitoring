from pydantic import BaseModel


class MachineState(BaseModel):
    machine_id: str
    machine_name: str

    temperature: float
    vibration: float
    power: float
    rpm: float
    pressure: float

    timestamp: str