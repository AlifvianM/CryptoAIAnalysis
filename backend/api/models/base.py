from pydantic import BaseModel
from datetime import datetime
from utils.enum import FieldType


class CustomBaseModel(BaseModel):
    """
    Custom BaseModel with global function, should be used instead of
    the default pydantic.BaseModel for easier global-level modification
    """

    class Config:
        arbitary_types_allowed = True

        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S"),
            FieldType: lambda v: v.value
        }