from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    """
    Homepage endpoint that displays a simple greeting message.

    Returns:
        str: An HTML string containing "Hello World".
    """
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
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
