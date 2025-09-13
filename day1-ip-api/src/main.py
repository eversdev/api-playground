import logging

from flask import Flask, request

app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.route("/")
def home():
    try:
        # x = 1/0  # Used to test endpoint-wide error handling, comment out in production
        """
        Homepage endpoint that displays a simple greeting message.

        Returns:
        str: An HTML string containing "Hello World".
        """
        lang_str = request.args.get("lang", "0")
        try:
            lang = int(lang_str)
        except ValueError as e:
            logging.exception("Invalid parameter")
            lang = 0

        agent = request.headers.get("User-Agent")
        try:
            agent = agent.upper()
        except AttributeError as e:
            logging.exception("Invalid method used, value is not a string")
            agent = ""

        logging.info(
            f"Received {request.method} at {request.path} from {request.remote_addr} "
            f"query param is {lang} and client is {agent}"
        )

        status_code = 200
        response_body = "<h1>Hello World</h1>"
        logging.info(f"Response sent | status: {status_code} | body: {response_body}")

        return "<h1>Hello World</h1>"
    except Exception as e:
        logging.exception("Unexpected error")
        return "<h1>Unexpected error</h1>", 500


@app.route("/greet/<name>")
def greet(name):
    try:
        # x = 1/0  # Used to test endpoint-wide error handling, comment out in production
        """
        Greeting endpoint that personalizes the response with the given name.

        Args:
            name (str): The name provided in the URL path.

        Returns:
            str: A greeting message that includes the given name.
        """
        lang_str = request.args.get("lang", "0")
        try:
            lang = int(lang_str)
        except ValueError as e:
            logging.exception("Invalid parameter")
            lang = 0

        agent = request.headers.get("User-Agent")
        try:
            agent = agent.upper()
        except AttributeError as e:
            logging.exception("Invalid method used, value is not a string")
            agent = ""

        logging.info(
            f"Received {request.method} at {name} from {request.remote_addr} "
            f"query param is {lang} and client is {agent}"
        )

        status_code = 200
        response_body = f"Hello {name}!"
        logging.info(f"Response sent | status: {status_code} | body: {response_body}")

        return f"Hello {name}!"
    except Exception as e:
        logging.exception("Unexpected error")
        return "<h1>Unexpected error</h1>", 500


if __name__ == "__main__":
    print("Started")
    app.run("0.0.0.0", port=5000, debug=True)
