import logging

import uvicorn
from fastapi import FastAPI, Request

logger = logging.getLogger("uvicorn")


app = FastAPI()


@app.get("/")
def home(request: Request):

    method = request.method
    url = request.url.path

    logger.info(f"The {method} method was called and the url path was {url}")

    return "Hello world"
