from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column("username", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)