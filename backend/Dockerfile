FROM python:3.10-slim

WORKDIR /backend/app

RUN pip install fastapi uvicorn

CMD uvicorn pip install fastapi

COPY app /backend/app

EXPOSE 8000

CMD uvicorn hello:app --host 0.0.0.0 --port 8000
