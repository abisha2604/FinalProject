from fastapi import Depends
from sqlalchemy.orm import Session
from database.get_db import get_db
from models.schema import History

def save_chat(db:Session, question: str, reply: str):
    chat = History(
        user_question=question,
        llm_reply=reply
    )
    db.add(chat)
    db.commit()

def get_history(db: Session):
    data = db.query(History).all()
    return data
    
def delete_history(db: Session):
    data = db.query(History).delete() 
    db.commit()
    return {"messages":"Deleted"}

def get_recent_history(db: Session, limit=5):
    return (db.query(History).order_by(History.id.desc()) .limit(limit).all()[::-1])

def build_memory(db: Session):
    history = get_recent_history(db)
    memory = ""

    for h in history:
        memory = memory + f"User: {h.user_question}\n"
        memory = memory + f"Assistant: {h.llm_reply}\n"

    return memory


