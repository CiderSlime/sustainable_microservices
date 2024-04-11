import os

from sqlalchemy.ext.asyncio import create_async_engine

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_STRING = f"postgresql+asyncpg://myuser:mypassword@{DB_HOST}:5432/mydb"


def get_engine():
    return create_async_engine(
        DB_STRING,
        echo=True,
        future=True,
    )


