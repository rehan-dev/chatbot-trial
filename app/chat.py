from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .config import settings
from openai import OpenAI

client = OpenAI(api_key=settings.openai_key)

router = APIRouter(prefix="/api/v1", tags=["Chatbot"])

def chatbot_response(msg: str):
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant and your name is Disrupt Bot"},
            {"role": "user", "content": msg}
        ],
        max_tokens=50,
    )
    return completion.choices[0].message.content

@router.post("/conversations/")
def create_conversation(data: schemas.ConversationCreate, db: Session = Depends(auth.get_db), user=Depends(auth.get_current_user)):
    convo = models.Conversation(user_id=user.id, title=data.title)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return {"id": convo.id, "title": convo.title}

@router.post("/conversations/{conversation_id}/message")
def send_message(conversation_id: int, data: schemas.MessageCreate, db: Session = Depends(auth.get_db), user=Depends(auth.get_current_user)):
    convo = db.query(models.Conversation).filter_by(id=conversation_id, user_id=user.id, is_deleted=False).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_msg = models.Message(conversation_id=convo.id, sender="user", content=data.content)
    db.add(user_msg)

    bot_reply = chatbot_response(data.content)
    bot_msg = models.Message(conversation_id=convo.id, sender="bot", content=bot_reply)
    db.add(bot_msg)

    db.commit()
    return {"response": bot_reply}

@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: int, db: Session = Depends(auth.get_db), user=Depends(auth.get_current_user)):
    convo = db.query(models.Conversation).filter_by(id=conversation_id, user_id=user.id, is_deleted=False).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = [{
        "sender": m.sender,
        "content": m.content,
        "timestamp": m.timestamp
    } for m in convo.messages]
    return {"id": convo.id, "messages": messages}


@router.get("/all-conversations")
def get_conversations(db: Session = Depends(auth.get_db), user=Depends(auth.get_current_user)):
    convos = db.query(models.Conversation).filter_by(user_id=user.id, is_deleted=False).all()
    if not convos:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convos

@router.delete("conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(auth.get_db), user=Depends(auth.get_current_user)):
    convo = db.query(models.Conversation).filter_by(id=conversation_id, user_id=user.id).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    convo.is_deleted = True # type: ignore
    db.commit()
    return {"message": "Message soft deleted"}
    
