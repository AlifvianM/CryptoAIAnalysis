from typing import Union

from fastapi import FastAPI
from agents.main import router as api_router
from agents.helper.test import get_test
from agents.graph_state.chat import run_chat
from dotenv import load_dotenv, dotenv_values

config = dotenv_values(".env")

# load_dotenv() 

app = FastAPI()
app.include_router(api_router, prefix='/api')


@app.get("/")
def read_root():
    return {"Hello": "World"}