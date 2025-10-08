import logging
import psycopg2
from pydantic import BaseModel

import sys

# print(sys.executable)

import uvicorn
from fastapi import FastAPI, Request, Body


class NewUser(BaseModel):
    first_name: str


logger = logging.getLogger("uvicorn")
app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)


app_logger.addHandler(handler)


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


@app.post("/add_user")
def add_user(new_user: NewUser = Body(...), request: Request = None):

    method = request.method if request else "N/A"
    host = request.client.host if request else "N/A"
    port = request.client.port if request else "N/A"

    app_logger.info(
        f"The endpoint used {method} and the host of the client "
        f" is {host}, and the port is {port}. The payload is "
        f"{new_user.first_name}"
    )

    with psycopg2.connect(
        user="admin", 
        password="password",
        dbname="postgres",
        port=5432, host="postgres"
    ) as db_connection:
        with db_connection.cursor() as cur:
            cur.execute("INSERT INTO users (fname) VALUES (%s)", (new_user.first_name,))
        db_connection.commit()
 

    return {"first_name": new_user.first_name}


@app.get("/test_volume")
def test_volume():
    app_logger.info("Volume mount test successful!")
    return {"message": "Volume mount test ✅"}
