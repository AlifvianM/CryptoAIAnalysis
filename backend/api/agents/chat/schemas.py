from pydantic import Field
from base.base_schemas import BaseResponse
from models.base import CustomBaseModel as BaseModel


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    response: str

class ChatModelResponse(BaseResponse):
    # data: list[ChatResponse]
    resp: str

