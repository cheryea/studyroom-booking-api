# schemas/facility.py

from pydantic import BaseModel, ConfigDict

class FacilityResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
