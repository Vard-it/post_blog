from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
# from pydantic import BaseSettings


# Stexic pydenticy vercnelua sa variablenery uppercase sarqi, kap chuni vor menq lowercase enq grel
# class Settings(BaseSettings):
#     database_password: str = "localhost"
#     database_username: str = "postgres"
#     secret_key: str = "51d5ew54c8d4v8d5s4cds654c8esd"


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Post Blog')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def main_function():
    return {"msg": "Hello world"}
