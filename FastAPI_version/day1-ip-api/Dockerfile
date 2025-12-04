# Use official Python 3.12 image as the base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy all application files into the container
COPY . /app

# Install Python dependencies from requirements.txt without caching
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI app using Uvicorn
# Replace 'fastapi_version.main:app' with the correct module path if different
CMD ["uvicorn", "fastapi_version.main:app", "--host", "0.0.0.0", "--port", "8000"]
