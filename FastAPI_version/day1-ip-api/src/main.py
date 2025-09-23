import logging
#import sys
#print(sys.executable)

import uvicorn
from fastapi import FastAPI, Request

logger = logging.getLogger("uvicorn")


app = FastAPI()


@app.get("/")
def home(request: Request):

    method = request.method
    url = request.url.path

    logger.info(f"The {method} method was called and the url path was {url}")

    return {"message": "Hello world"}



@app.get("/hello/{name}")
def greeting(name: str):
    return {"hello": name}

@app.get("/sum")
def calculate_sum(a:int, b:int):
    return {"sum": a + b}
