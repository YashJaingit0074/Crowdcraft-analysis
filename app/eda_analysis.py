import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class EngagementEDA:
    def __init__(self, database_url):
        self.engine = create_engine(database_url.replace('+asyncpg', ''))
        
    def load_data(self):
        """Load data from database for analysis"""
        # Load events data
        events_query = """
        SELECT e.*, u.username, s.started_at as session_start, s.ended_at as session_end
        FROM events e
        JOIN users u ON e.user_id = u.id
        LEFT JOIN sessions s ON e.session_id = s.id
        """
        self.events_df = pd.read_sql(events_query, self.engine)
        self.events_df['timestamp'] = pd.to_datetime(self.events_df['timestamp'])
        
        # Load sessions data
        sessions_query = """
        SELECT s.*, u.username
        FROM sessions s
        JOIN users u ON s.user_id = u.id
        """
        self.sessions_df = pd.read_sql(sessions_query, self.engine)
        self.sessions_df['started_at'] = pd.to_datetime(self.sessions_df['started_at'])
        self.sessions_df['ended_at'] = pd.to_datetime(self.sessions_df['ended_at'])
        
    def analyze_user_engagement_patterns(self):
        """Identify user engagement patterns and trends"""
        print("🔍 USER ENGAGEMENT ANALYSIS")
        print("=" * 50)
        
        # Basic statistics
        total_users = self.events_df['user_id'].nunique()
        total_events = len(self.events_df)
        total_sessions = len(self.sessions_df)
        
        print(f"📊 Basic Metrics:")
        print(f"   Total Users: {total_users}")
        print(f"   Total Events: {total_events}")
        print(f"   Total Sessions: {total_sessions}")
        print(f"   Avg Events per User: {total_events/total_users:.2f}")
        
        # Event type distribution
        event_counts = self.events_df['event_type'].value_counts()
        print(f"\n📈 Event Type Distribution:")
        for event_type, count in event_counts.items():
            percentage = (count / total_events) * 100
            print(f"   {event_type}: {count} ({percentage:.1f}%)")
            
        return {
            'total_users': total_users,
            'total_events': total_events,
            'event_distribution': event_counts.to_dict()
        }
    
    def identify_user_engagement_strengths(self):
        """Identify high-engagement users and successful patterns"""
        print("\n🌟 ENGAGEMENT STRENGTHS ANALYSIS")
        print("=" * 50)
        
        # User activity analysis
        user_activity = self.events_df.groupby('username').agg({
            'id': 'count',  # total events
            'session_id': 'nunique',  # unique sessions
            'timestamp': ['min', 'max']  # first and last activity
        }).round(2)
        
        user_activity.columns = ['total_events', 'unique_sessions', 'first_activity', 'last_activity']
        user_activity['avg_events_per_session'] = user_activity['total_events'] / user_activity['unique_sessions']
        user_activity = user_activity.sort_values('total_events', ascending=False)
        
        # Top engaged users
        top_users = user_activity.head(10)
        print("🏆 Top 10 Most Engaged Users:")
        for idx, (username, data) in enumerate(top_users.iterrows(), 1):
            print(f"   {idx}. {username}: {data['total_events']} events, {data['unique_sessions']} sessions")
        
        # Engagement patterns
        highly_engaged = user_activity[user_activity['total_events'] > user_activity['total_events'].quantile(0.8)]
        print(f"\n💪 High Engagement Pattern (Top 20%):")
        print(f"   Average Events: {highly_engaged['total_events'].mean():.1f}")
        print(f"   Average Sessions: {highly_engaged['unique_sessions'].mean():.1f}")
        print(f"   Average Events/Session: {highly_engaged['avg_events_per_session'].mean():.1f}")
        
        return user_activity, highly_engaged
    
    def analyze_temporal_patterns(self):
        """Analyze engagement patterns over time"""
        print("\n⏰ TEMPORAL ENGAGEMENT PATTERNS")
        print("=" * 50)
        
        # Daily activity patterns
        self.events_df['hour'] = self.events_df['timestamp'].dt.hour
        self.events_df['day_of_week'] = self.events_df['timestamp'].dt.day_name()
        
        # Peak hours
        hourly_activity = self.events_df.groupby('hour')['id'].count()
        peak_hour = hourly_activity.idxmax()
        print(f"🕐 Peak Activity Hour: {peak_hour}:00 ({hourly_activity[peak_hour]} events)")
        
        # Peak days
        daily_activity = self.events_df.groupby('day_of_week')['id'].count()
        peak_day = daily_activity.idxmax()
        print(f"📅 Peak Activity Day: {peak_day} ({daily_activity[peak_day]} events)")
        
        return hourly_activity, daily_activity
    
    def identify_optimization_opportunities(self):
        """Identify areas for optimization based on EDA"""
        print("\n🎯 OPTIMIZATION STRATEGIES")
        print("=" * 50)
        
        user_activity, highly_engaged = self.identify_user_engagement_strengths()
        
        # Low engagement users
        low_engaged = user_activity[user_activity['total_events'] <= user_activity['total_events'].quantile(0.2)]
        print(f"⚠️  Low Engagement Users (Bottom 20%): {len(low_engaged)} users")
        print(f"   Average Events: {low_engaged['total_events'].mean():.1f}")
        
        # Session analysis
        avg_session_length = self.sessions_df.dropna(subset=['ended_at']).apply(
            lambda x: (x['ended_at'] - x['started_at']).total_seconds() / 60, axis=1
        ).mean()
        
        print(f"\n📊 Session Insights:")
        print(f"   Average Session Length: {avg_session_length:.1f} minutes")
        
        # Recommendations
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        print(f"   1. Target {len(low_engaged)} low-engagement users with personalized campaigns")
        print(f"   2. Optimize features during peak hours ({self.analyze_temporal_patterns()[0].idxmax()}:00)")
        print(f"   3. Focus on increasing session length (current avg: {avg_session_length:.1f}min)")
        print(f"   4. Replicate high-engagement patterns across user base")
        
        return {
            'low_engagement_count': len(low_engaged),
            'avg_session_length': avg_session_length,
            'optimization_targets': low_engaged.index.tolist()[:5]  # Top 5 users to target
        }
    
    def create_engagement_visualizations(self):
        """Create visualizations for engagement analysis"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Event Types Distribution', 'Hourly Activity Pattern', 
                          'Daily Activity Pattern', 'User Engagement Levels'),
            specs=[[{'type': 'pie'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'histogram'}]]
        )
        
        # Event types pie chart
        event_counts = self.events_df['event_type'].value_counts()
        fig.add_trace(
            go.Pie(labels=event_counts.index, values=event_counts.values, name="Event Types"),
            row=1, col=1
        )
        
        # Hourly activity
        hourly_activity = self.events_df.groupby('hour')['id'].count()
        fig.add_trace(
            go.Bar(x=hourly_activity.index, y=hourly_activity.values, name="Hourly Activity"),
            row=1, col=2
        )
        
        # Daily activity
        daily_activity = self.events_df.groupby('day_of_week')['id'].count()
        fig.add_trace(
            go.Bar(x=daily_activity.index, y=daily_activity.values, name="Daily Activity"),
            row=2, col=1
        )
        
        # User engagement distribution
        user_events = self.events_df.groupby('username')['id'].count()
        fig.add_trace(
            go.Histogram(x=user_events.values, name="User Engagement Distribution"),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, title_text="User Engagement Analytics Dashboard")
        return fig
    
    def run_complete_analysis(self):
        """Run complete EDA analysis"""
        print("🚀 STARTING COMPREHENSIVE ENGAGEMENT EDA")
        print("=" * 60)
        
        self.load_data()
        
        # Run all analyses
        basic_metrics = self.analyze_user_engagement_patterns()
        user_activity, highly_engaged = self.identify_user_engagement_strengths()
        hourly_activity, daily_activity = self.analyze_temporal_patterns()
        optimization_insights = self.identify_optimization_opportunities()
        
        # Create visualizations
        dashboard = self.create_engagement_visualizations()
        
        print("\n✅ EDA ANALYSIS COMPLETE")
        print("📈 Insights generated for feature prioritization and user engagement optimization")
        
        return {
            'basic_metrics': basic_metrics,
            'user_activity': user_activity,
            'temporal_patterns': {
                'hourly': hourly_activity,
                'daily': daily_activity
            },
            'optimization_insights': optimization_insights,
            'dashboard': dashboard
        }


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/analytics')
    
    eda = EngagementEDA(db_url)
    results = eda.run_complete_analysis()
