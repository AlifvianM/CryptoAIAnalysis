from models.base import CustomBaseModel as BaseModel
from pydantic import Field


class BaseResponse(BaseModel):
    status: str = Field(default="success")
    message: str = Field(default="")