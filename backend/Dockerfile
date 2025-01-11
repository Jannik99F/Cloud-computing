FROM python:3.10-slim

WORKDIR /backend/app

RUN pip install --no-cache-dir fastapi uvicorn psycopg2-binary alembic sqlmodel python-dotenv

COPY ./app /backend/app

EXPOSE 8000

# Define the command to run when the container starts
CMD ["uvicorn", "hello:app", "--host", "0.0.0.0", "--port", "8000"]
