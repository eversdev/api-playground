# API Playground

## Description
This project demonstrates the practical use of APIs with Flask.  
It provides two simple HTTP endpoints that return string responses.

### Requirements
- Python 3.11+
- Flask
- pytest (for testing)
- Docker (optional)

## Installation
Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```
Optionally, build and run a Docker container:

```bash
docker build -t api-playground .
docker run -p 5000:5000 api-playground 
```

How to Run the App

You can run the app in two ways:

Terminal: Use curl to access endpoints:

```bash
curl http://localhost:5000/
curl http://localhost:5000/greet/John
```
Browser: Open a web browser and navigate to:
```bash
http://localhost:5000/
http://localhost:5000/greet/John
```

## Endpoints

GET / → Returns:
```bash
Hello World
```

GET /greet/<name> → Returns:
```bash
Hello John
```

## Testing
```bash
pytest -v
```
This verifies that both endpoints return the expected responses.

## Docker
The project can be containerized:

1. Build the Docker image:
```bash
docker build -t api-playground .
```
2. Run the container:
```bash
docker run -p 5000:5000 api-playground
```

3. Access the endpoints via browser or curl as shown above.

