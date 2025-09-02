from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId



class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    # manual validation
    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project id must be alphanumeric')
        
        return value

class Config:
    arbitrary_typed_allowed = True