from sqlalchemy.ext.asyncio import create_async_engine


DB_STRING = "postgresql+asyncpg://myuser:mypassword@localhost:5432/mydb"


def get_engine():
    return create_async_engine(
        DB_STRING,
        echo=True,
        future=True,
    )


