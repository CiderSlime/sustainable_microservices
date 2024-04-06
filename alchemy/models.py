import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    UUID,
    String,
    ForeignKey,
    Enum,
    Date,
    Double
)
from sqlalchemy.orm import declarative_base, mapped_column, relationship

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    uid = Column(UUID, primary_key=True)
    value = Column(Integer, nullable=False)
    latency = Column(Integer, nullable=False)
    customer_id = Column(UUID, ForeignKey("customers.uid"), nullable=False)
    status = Column(String, nullable=False)


class Customer(Base):
    __tablename__ = "customers"

    uid = Column(UUID, primary_key=True)
    password = Column(String(64), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, nullable=False)
    gender = Column(String)
    phone_number = Column(String)
    social_insurance_number = Column(String)
    avatar = Column(String)
    date_of_birth = Column(Date)
    email = Column(String)
    balance = Column(Double, nullable=False)
    # employment = Column(Integer, ForeignKey("employments.id"))
    # credit_card = Column(Integer, ForeignKey("credit_cards.id"), nullable=False)
    # address = Column(Integer, ForeignKey("addresses.id"))
    created_at = Column(Date, nullable=False, default=datetime.utcnow)
    updated_at = Column(Date, nullable=False, default=datetime.utcnow)


# class Employment:
#     __tablename__ = "employments"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     key_skill = Column(String)
#
#
# class CreditCard:
#     __tablename__ = "credit_cards"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     balance = Column(Float, nullable=False)
#     cc_number = Column(String)
#
#
# class Address:
#     __tablename__ = "addresses"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     country = Column(String)
#     state = Column(String)
#     street_address = Column(String)
#     street_name = Column(String)
#     zip_code = Column(String)
