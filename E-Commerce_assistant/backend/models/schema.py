from sqlalchemy import Column, Integer, String
from datetime import datetime
from database.db import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class History(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String, nullable=False)
    llm_reply = Column(String, nullable=False)

Base.metadata.create_all(engine)
