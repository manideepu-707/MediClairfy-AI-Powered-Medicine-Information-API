from typing import Optional
from pydantic import BaseModel, Field, field_validator

class Medic(BaseModel):
    name: str=Field(..., min_length=2, max_length=100)
    medical_usage: Optional[str]=None
    side_effects : Optional[str]=None
    warnings : Optional[str]=None
    age_restriction : Optional[str]=None

    @field_validator('name')
    @classmethod
    def name_validation(cls,v:str):
        return v.strip().lower()



