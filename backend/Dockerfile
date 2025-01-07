# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Copy the current directory contents into the container at /app
COPY ./app /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run Uvicorn with your FastAPI app
CMD ["uvicorn", "hello:app", "--host", "0.0.0.0", "--port", "8000"]
