# Use the official Python 3.11 slim image as the base
FROM python:3.11
ENV PYTHONUNBUFFERED=1


# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . /app


# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow access to the Flask app
EXPOSE 5000


# Command to run the Flask application
CMD ["python", "src/main.py"]