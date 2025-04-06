from fastapi import APIRouter
from agents.chat.views import router as chat_router

router = APIRouter()
router.include_router(chat_router)