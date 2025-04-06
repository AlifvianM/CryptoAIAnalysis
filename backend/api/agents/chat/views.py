from agents.graph_state.chat import run_chat
from agents.chat.schemas import ChatModelResponse,ChatRequest

from fastapi import APIRouter, Request, Response, HTTPException

router = APIRouter(prefix="/chat")
tag = "Chat"

@router.post("", response_model=ChatModelResponse, tags=[tag])
def chat(
    request: Request,
    response: Response,
    question: ChatRequest
):
    try:
        resp_data = run_chat(content=question)
        return ChatModelResponse(
            resp=resp_data,
            message="Success asking model"
        )
    
    except HTTPException as ex:
        response.status_code = ex.status_code
        return ChatModelResponse(
            status="Error",
            message=ex.detail
        )
    
    except Exception as ex:
        response.status_code = 500
        return ChatModelResponse(
            status="Error",
            message="Failed asking the model"
        )