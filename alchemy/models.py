from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=False)
    latency = Column(Integer, nullable=False)
    customer_id = Column(String(255), nullable=False)
