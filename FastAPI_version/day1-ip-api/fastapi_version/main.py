import logging
import psycopg2
from typing import Optional
from psycopg2 import OperationalError, IntegrityError, DataError

from pydantic import BaseModel

import sys
import os

# print(sys.executable)

import uvicorn
from fastapi import FastAPI, Request, Body, Response

# Environment flag
TEST_MODE = os.getenv("TEST_MODE", "0") == "1"


# Production-safe model
class NewUser(BaseModel):
    first_name: str
    department_id: int


# Test model for constraint violations
class NewUserTest(BaseModel):
    first_name: Optional[str] = None  # allows NULL testing
    department_id: Optional[int] = None  # allows FK violation testing


logger = logging.getLogger("uvicorn")
app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

app_logger.addHandler(handler)

app = FastAPI()

counter_home = 0
counter_hello = 0
counter_sum = 0
counter_add_user = 0

network_service_error = ["Connection refused", "could not connect to server", "TCP/IP", "timeout"]
credentials_error = ["password authentication failed", "role does not exist", "FATAL", "database"]
constraint_error = ["null value in column", "duplicate key value violates unique", "violates foreign key constraint"]


@app.get("/")
def home(request: Request):
    global counter_home
    counter_home += 1

    method = request.method
    url = request.url.path

    logger.info(f"The {method} method was called and the url path was {url}")
    app_logger.info(f"Counter request for / endpoint: {counter_home}")

    return {"message": "Hello world"}


@app.get("/hello/{name}")
def greeting(request: Request, name: str):
    global counter_hello
    counter_hello += 1

    method = request.method
    url = request.url.path

    logger.info(
        f"The method used was {method}, the URL path was {url}, "
        f"and the path parameter was {name}"
    )

    app_logger.info(f'Counter request for /hello/{{name}} endpoint: {counter_hello}')

    return {"hello": name}


@app.get("/sum")
def calculate_sum(request: Request, a: int, b: int):
    global counter_sum
    counter_sum += 1

    method = request.method

    logger.info(
        f"The method used is {method} and the " f"query parameters are {a} and {b}"
    )

    app_logger.info(f"Counter request for /sum endpoint: {counter_sum}")

    return {"sum": a + b}


@app.post("/add_user")
def add_user(request: Request, incoming_user: dict = Body(...)):
    global counter_add_user
    counter_add_user += 1

    method = request.method
    host = request.client.host
    port = request.client.port

    # Dynamically select model based on TEST_MODE
    model_class = NewUserTest if TEST_MODE else NewUser
    new_user = model_class(**incoming_user)

    app_logger.info(
        f"The endpoint used {method} and the host of the client "
        f" is {host}, and the port is {port}. The payload is "
        f"{new_user.dict()}"
    )
    try:
        with psycopg2.connect(
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                dbname=os.environ["POSTGRES_DB"],
                port=int(os.environ.get("POSTGRES_PORT", 5432)),
                host="postgres",
        ) as db_connection:
            with db_connection.cursor() as cur:
                cur.execute("INSERT INTO users (fname, department_id) VALUES (%s, %s)",
                            (new_user.first_name, new_user.department_id), )
            db_connection.commit()
    except IntegrityError as e:
        error_msg = ' '.join(str(e).split())
        if any(key in str(e) for key in constraint_error):
            app_logger.warning(f"Constraint violation while inserting user '{new_user.first_name}': "
                               f"check NOT NULL, UNIQUE, or foreign key constraints"
                               )
    except OperationalError as e:
        error_msg = ' '.join(str(e).split())  # normalize spaces

        if any(key in str(e) for key in network_service_error):
            app_logger.warning(f"Network/service error while connecting to DB — check host/port or DB service")

        elif any(key in str(e) for key in credentials_error):
            app_logger.warning(f"Invalid DB credentials: check username, password, or database name")

        app_logger.warning(f"DB connection failed {error_msg}")
    except DataError as e:
        error_msg = ' '.join(str(e).split())
        app_logger.warning(
            f"Data error while inserting user '{new_user.first_name}': "
            f"check column data types or value ranges — {error_msg}"
        )


        app_logger.info(f"Counter request for add_user endpoint: {counter_add_user}")

    return {"first_name": new_user.first_name}


@app.get("/metrics")
def metrics():
    metrics_counters = {
        "home_requests_total": counter_home,
        "hello_requests_total": counter_hello,
        "sum_requests_total": counter_sum,
        "add_user_requests_total": counter_add_user
    }


    lines = [f"{key} {value}" for key, value in metrics_counters.items()]
    text = "\n".join(lines)

    return Response(content=text, media_type="text/plain")
