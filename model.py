from sqlalchemy import Column, String ,Integer
from pydantic import BaseModel
from config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column (String)
    email = Column(String)
    password = Column(String)

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True,autoincrement=True)
    msg = Column(String)

  