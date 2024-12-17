from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

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
    data: str | None = None # Making parameter optional

@application.get("/")
async def home_route():
    return {"message": "Home Route"}

# @application.post("/embedding_route")
# async def vector_database(request: Request, item: Item):


