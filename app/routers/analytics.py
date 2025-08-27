from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import SessionLocal
from app.models import Event

router = APIRouter(prefix="/analytics", tags=["analytics"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/event_counts")
async def get_event_counts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event.event_type, func.count()).group_by(Event.event_type))
    return {"event_counts": dict(result.all())}
