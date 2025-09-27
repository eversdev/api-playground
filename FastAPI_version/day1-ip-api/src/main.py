import logging
import psycopg2

# import sys
# print(sys.executable)

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
def greeting(request: Request, name: str):
    method = request.method
    url = request.url.path

    logger.info(
        f"The method used was {method}, the URL path was {url}, "
        f"and the path parameter was {name}"
    )

    return {"hello": name}


@app.get("/sum")
def calculate_sum(request: Request, a: int, b: int):

    method = request.method

    logger.info(
        f"The method used is {method} and the " f"query parameters are {a} and {b}"
    )

    return {"sum": a + b}


db_connection = psycopg2.connect(
    user="admin", password="password", dbname="postgres", host="postgres", port=5432
)

cur = db_connection.cursor()
cur.execute("SELECT 1")
result = cur.fetchone()
logger.info(f"Postgres test result: {result}")
cur.close()
