from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import SessionLocal
from app.eda_analysis import EngagementEDA
from dotenv import load_dotenv
import os
import asyncio

router = APIRouter(prefix="/eda", tags=["eda-analysis"])

load_dotenv()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/engagement-analysis")
async def run_engagement_analysis():
    """Run comprehensive EDA analysis on user engagement data"""
    try:
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/analytics')
        # Convert async URL to sync for pandas
        sync_db_url = db_url.replace('+asyncpg', '')
        
        eda = EngagementEDA(sync_db_url)
        results = eda.run_complete_analysis()
        
        # Convert non-serializable objects
        serializable_results = {
            'basic_metrics': results['basic_metrics'],
            'top_users': results['user_activity'].head(10).to_dict('index'),
            'temporal_patterns': {
                'peak_hour': results['temporal_patterns']['hourly'].idxmax(),
                'peak_day': results['temporal_patterns']['daily'].idxmax(),
                'hourly_distribution': results['temporal_patterns']['hourly'].to_dict(),
                'daily_distribution': results['temporal_patterns']['daily'].to_dict()
            },
            'optimization_insights': results['optimization_insights']
        }
        
        return {
            "status": "success",
            "message": "EDA analysis completed successfully",
            "insights": serializable_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EDA analysis failed: {str(e)}")

@router.get("/user-strengths")
async def analyze_user_strengths():
    """Identify high-performing users and engagement patterns"""
    try:
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/analytics')
        sync_db_url = db_url.replace('+asyncpg', '')
        
        eda = EngagementEDA(sync_db_url)
        eda.load_data()
        user_activity, highly_engaged = eda.identify_user_engagement_strengths()
        
        return {
            "status": "success",
            "top_performers": user_activity.head(10).to_dict('index'),
            "high_engagement_patterns": {
                "avg_events": float(highly_engaged['total_events'].mean()),
                "avg_sessions": float(highly_engaged['unique_sessions'].mean()),
                "avg_events_per_session": float(highly_engaged['avg_events_per_session'].mean())
            },
            "recommendations": [
                "Analyze top performers' behavior patterns",
                "Implement gamification for low-engagement users",
                "Create personalized content based on high-performers' preferences"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User strength analysis failed: {str(e)}")

@router.get("/optimization-strategies")
async def get_optimization_strategies():
    """Get data-driven optimization strategies"""
    try:
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/analytics')
        sync_db_url = db_url.replace('+asyncpg', '')
        
        eda = EngagementEDA(sync_db_url)
        eda.load_data()
        optimization_insights = eda.identify_optimization_opportunities()
        
        return {
            "status": "success",
            "optimization_opportunities": optimization_insights,
            "action_items": [
                f"Target {optimization_insights['low_engagement_count']} low-engagement users",
                f"Optimize session length (current: {optimization_insights['avg_session_length']:.1f}min)",
                "Implement retention strategies for identified at-risk users",
                "A/B test features during peak engagement hours"
            ],
            "priority_users": optimization_insights['optimization_targets']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization analysis failed: {str(e)}")
