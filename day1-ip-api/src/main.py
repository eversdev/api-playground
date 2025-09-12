import logging

from flask import Flask, request

app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.route("/")
def home():
    """
    Homepage endpoint that displays a simple greeting message.

    Returns:
        str: An HTML string containing "Hello World".
    """
    lang = request.args.get("lang")
    agent = request.headers.get("User-Agent")

    logging.info(
        f"Received {request.method} at {request.path} from {request.remote_addr}"
        f" query param is {lang} and client is {agent}"
    )

    return "<h1>Hello World</h1>"


@app.route("/greet/<name>")
def greet(name):
    """
    Greeting endpoint that personalizes the response with the given name.

    Args:
        name (str): The name provided in the URL path.

    Returns:
        str: A greeting message that includes the given name.
    """
    lang = request.args.get("lang")
    agent = request.headers.get("User-Agent")

    logging.info(
        f"Received {request.method} at {name} from {request.remote_addr}"
        f"query param is {lang} and client is {agent}"
    )

    return f"Hello {name}!"


if __name__ == "__main__":
    print("Started")
    app.run("0.0.0.0", port=5000, debug=True)
