from fastapi import FastAPI
from starlette.requests import Request


app = FastAPI()


@app.get("/")
def index(request: Request):
    return "Hello world"