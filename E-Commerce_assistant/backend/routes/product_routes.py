from fastapi import Depends, APIRouter
from database.get_db import get_db
from models.pydantic import Products
from models.schema import History
from sqlalchemy.orm import Session
from services.rag_service import pipeline
from services.data_service import save_chat, get_history, delete_history

router = APIRouter()

@router.post("/chat")
def create_chat(data:Products, db:Session=Depends(get_db)):
    question = data.query        
    reply = pipeline(db,question)    
    save_chat(db, question, reply)
    return reply

@router.get("/history")
def history(db: Session = Depends(get_db)):
    return get_history(db) 

@router.delete("/delete-history")
def delete(db: Session = Depends(get_db)):
    return delete_history(db)
