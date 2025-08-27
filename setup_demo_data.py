import asyncio
from sqlalchemy import text
from app.database import SessionLocal
from app.models import User, Session, Event
import random
from datetime import datetime, timedelta

async def create_sample_engagement_data():
    """Create comprehensive sample data for demonstration"""
    
    print("🚀 Creating sample engagement data...")
    
    async with SessionLocal() as db:
        # Check if data already exists
        result = await db.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        
        if user_count > 0:
            print(f"✅ Sample data already exists ({user_count} users)")
            return
        
        # Create sample users with realistic names
        user_names = [
            "alice_data", "bob_analyst", "charlie_dev", "diana_manager", "eve_designer",
            "frank_engineer", "grace_scientist", "henry_student", "iris_researcher", "jack_admin",
            "kate_marketer", "leo_developer", "maya_analyst", "noah_intern", "olivia_lead",
            "paul_consultant", "quinn_freelancer", "ruby_designer", "sam_engineer", "tina_product"
        ]
        
        users = []
        for name in user_names:
            user = User(username=name)
            db.add(user)
            users.append(user)
        
        await db.commit()
        
        # Refresh to get IDs
        for user in users:
            await db.refresh(user)
        
        # Create realistic sessions and events
        event_types = ['login', 'page_view', 'click', 'search', 'purchase', 'logout', 'download', 'share', 'comment', 'like']
        
        total_sessions = 0
        total_events = 0
        
        for user in users:
            # Create 5-15 sessions per user over last 30 days
            num_sessions = random.randint(5, 15)
            
            for session_idx in range(num_sessions):
                # Create session with realistic timing
                days_ago = random.randint(0, 30)
                session_hour = random.choices(
                    [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                    weights=[5, 8, 10, 8, 12, 15, 12, 10, 8, 6, 4, 3, 2]
                )[0]
                
                session_start = datetime.now() - timedelta(
                    days=days_ago,
                    hours=random.randint(0, 23-session_hour),
                    minutes=random.randint(0, 59)
                )
                
                # Session length: 5-120 minutes with realistic distribution
                session_duration = random.choices(
                    [5, 15, 30, 45, 60, 90, 120],
                    weights=[20, 25, 20, 15, 10, 7, 3]
                )[0]
                
                session_end = session_start + timedelta(minutes=session_duration)
                
                session = Session(
                    user_id=user.id,
                    started_at=session_start,
                    ended_at=session_end
                )
                db.add(session)
                await db.commit()
                await db.refresh(session)
                total_sessions += 1
                
                # Create realistic events for this session
                # More events for longer sessions
                base_events = max(3, int(session_duration / 10))
                num_events = random.randint(base_events, base_events + 10)
                
                session_events = []
                for event_idx in range(num_events):
                    # Event timing within session
                    event_offset = random.randint(0, int(session_duration * 0.9))
                    event_time = session_start + timedelta(minutes=event_offset)
                    
                    # Realistic event type distribution
                    if event_idx == 0:
                        event_type = 'login'
                    elif event_idx == num_events - 1:
                        event_type = 'logout'
                    else:
                        event_type = random.choices(
                            event_types[1:-1],  # Exclude login/logout for middle events
                            weights=[25, 20, 15, 8, 5, 10, 8, 5, 4]  # page_view most common
                        )[0]
                    
                    event = Event(
                        user_id=user.id,
                        session_id=session.id,
                        event_type=event_type,
                        timestamp=event_time
                    )
                    session_events.append(event)
                    db.add(event)
                    total_events += 1
                
                # Commit all events for this session
                await db.commit()
        
        print(f"✅ Sample data created successfully!")
        print(f"   👥 Users: {len(users)}")
        print(f"   📊 Sessions: {total_sessions}")
        print(f"   ⚡ Events: {total_events}")
        print(f"   📈 Avg Events per User: {total_events / len(users):.1f}")
        print(f"   🎯 Avg Session Length: {total_sessions / len(users):.1f}")

if __name__ == "__main__":
    asyncio.run(create_sample_engagement_data())
