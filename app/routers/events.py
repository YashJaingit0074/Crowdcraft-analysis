from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.models import Event
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])

class EventCreate(BaseModel):
    user_id: int
    session_id: int
    event_type: str
    timestamp: datetime = None

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/")
async def log_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    db_event = Event(
        user_id=event.user_id,
        session_id=event.session_id,
        event_type=event.event_type,
        timestamp=event.timestamp or datetime.utcnow()
    )
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event
