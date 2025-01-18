import os
from sqlmodel import SQLModel, Session, create_engine, SQLModel

class DatabaseManager:
    _engine = None

    @staticmethod
    def initialize():
        database_url = os.getenv("DB_URL_LOCAL") if os.getenv("DEBUG") == "true" else os.getenv("DB_URL_PROD")

        DatabaseManager._engine = create_engine(database_url)
        SQLModel.metadata.create_all(DatabaseManager._engine)

    @staticmethod
    def get_engine():
        return DatabaseManager._engine

    @staticmethod
    def get_session():
        return Session(DatabaseManager._engine)