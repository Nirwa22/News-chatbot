from agent_executor import AgentReact
from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import json

load_dotenv()
Api_token = os.getenv("Api-token")
application = FastAPI()

# Cors enabled
application.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000",
                   "http://localhost:5000",
                   "http://localhost"
                  ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Item(BaseModel):
    query: str
    chat_history: str | None = None
    data: bytes | None = None


@application.get("/")
async def home_route():
    return {"message": "Home Route"}


@application.post("/embedding_route")
async def vector_database(request: Request, item: Item):
    api = request.headers.get("Authorization")
    if api == Api_token:
        query = item.query
        if query:
            chat_history = item.chat_history
            chat_history = chat_history + f"Human: {query}"
            # print(chat_history)
            output = AgentReact().agent_execution(chat_history)["output"]
            return output
        else:
            return {"message": "Please enter your query"}
    elif api and api != Api_token:
        return {"message": "Unauthorized access"}
    else:
        return {"message": "Api key needed"}



