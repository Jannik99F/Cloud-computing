FROM python:3.10-slim

WORKDIR /backend

RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary alembic sqlmodel python-dotenv celery redis azure-storage-blob python-multipart

# Copy alembic files
COPY ./alembic /backend/alembic
COPY ./alembic.ini /backend/alembic.ini

# Copy application files
COPY ./app /backend/app

WORKDIR /backend/app

EXPOSE 8000

# Define the command to run when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
