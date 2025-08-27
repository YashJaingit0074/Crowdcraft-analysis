import asyncio
from app.models import User, Session, Event
from app.database import SessionLocal, engine, Base
from datetime import datetime, timedelta
import random

async def create_sample_data():
    """Create sample data for EDA demonstration"""
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with SessionLocal() as db:
        # Create sample users
        users = []
        for i in range(20):
            user = User(username=f"user_{i+1}")
            db.add(user)
            users.append(user)
        
        await db.commit()
        
        # Refresh to get IDs
        for user in users:
            await db.refresh(user)
        
        # Create sample sessions and events
        event_types = ['login', 'click', 'page_view', 'purchase', 'logout', 'search', 'like', 'comment']
        
        for user in users:
            # Create 3-10 sessions per user
            num_sessions = random.randint(3, 10)
            
            for _ in range(num_sessions):
                # Create session
                session_start = datetime.now() - timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                session_end = session_start + timedelta(minutes=random.randint(5, 120))
                
                session = Session(
                    user_id=user.id,
                    started_at=session_start,
                    ended_at=session_end
                )
                db.add(session)
                await db.commit()
                await db.refresh(session)
                
                # Create 5-30 events per session
                num_events = random.randint(5, 30)
                
                for _ in range(num_events):
                    event_time = session_start + timedelta(
                        minutes=random.randint(0, int((session_end - session_start).total_seconds() / 60))
                    )
                    
                    event = Event(
                        user_id=user.id,
                        session_id=session.id,
                        event_type=random.choice(event_types),
                        timestamp=event_time
                    )
                    db.add(event)
                
        await db.commit()
        print("✅ Sample data created successfully!")
        print(f"   - {len(users)} users")
        print(f"   - Multiple sessions per user")
        print(f"   - Multiple events per session with various types")

if __name__ == "__main__":
    asyncio.run(create_sample_data())
