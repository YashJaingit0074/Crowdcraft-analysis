import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
import random
import json

# Page configuration
st.set_page_config(
    page_title="CrowdCraft Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.feature-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
.metric-card {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}
.quiz-option {
    background: #e3f2fd;
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-radius: 5px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_question' not in st.session_state:
    st.session_state.quiz_question = 0
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'quiz_topics_performance' not in st.session_state:
    st.session_state.quiz_topics_performance = {}

# Sidebar navigation
st.sidebar.title("🚀 CrowdCraft Analytics")
st.sidebar.markdown("---")

# Navigation options
page = st.sidebar.selectbox(
    "Choose a feature:",
    ["🏠 Home", "📊 Dashboard", "⚡ Real-time Analytics", "🔬 EDA Analysis", 
     "🎮 Interactive Games", "🧠 Quiz Challenge", "📚 Tutorial"]
)

# Generate unified sample data function
@st.cache_data
def generate_unified_data():
    """Generate unified analytics data for entire platform"""
    np.random.seed(42)
    
    # User data
    users = []
    for i in range(100):
        users.append({
            'user_id': i + 1,
            'username': f'user_{i+1}',
            'email': f'user_{i+1}@example.com',
            'created_at': datetime.now() - timedelta(days=random.randint(1, 365)),
            'last_active': datetime.now() - timedelta(hours=random.randint(0, 72))
        })
    
    # Events data - unified across platform
    events = []
    event_types = ['login', 'logout', 'click', 'scroll', 'purchase', 'view_page', 'download', 
                   'quiz_start', 'quiz_answer', 'quiz_complete', 'dashboard_view', 'eda_analysis']
    
    for i in range(2000):  # More events for better analytics
        events.append({
            'event_id': i + 1,
            'user_id': random.randint(1, 100),
            'event_type': random.choice(event_types),
            'timestamp': datetime.now() - timedelta(hours=random.randint(0, 720)),
            'page': f'/page_{random.randint(1, 10)}',
            'duration': random.randint(10, 300),
            'session_id': f'session_{random.randint(1, 200)}'
        })
    
    # Quiz performance data - part of unified system
    quiz_events = []
    topics = ['Basic Analytics', 'Data Visualization', 'Statistical Analysis', 'User Engagement']
    
    for i in range(500):  # Quiz-specific events
        quiz_events.append({
            'quiz_id': i + 1,
            'user_id': random.randint(1, 100),
            'topic': random.choice(topics),
            'question_id': random.randint(1, 20),
            'is_correct': random.choice([True, False]),
            'timestamp': datetime.now() - timedelta(hours=random.randint(0, 168)),
            'difficulty': random.choice(['Easy', 'Medium', 'Hard']),
            'response_time': random.randint(5, 30)
        })
    
    return pd.DataFrame(users), pd.DataFrame(events), pd.DataFrame(quiz_events)

# Load unified data
users_df, events_df, quiz_df = generate_unified_data()

# Add calculated fields to unified data
events_df['date'] = pd.to_datetime(events_df['timestamp']).dt.date
events_df['hour'] = pd.to_datetime(events_df['timestamp']).dt.hour
events_df['day_of_week'] = pd.to_datetime(events_df['timestamp']).dt.day_name()

# Real-time metrics calculation
current_time = datetime.now()
recent_events = events_df[pd.to_datetime(events_df['timestamp']) > current_time - timedelta(minutes=60)]
active_users = recent_events['user_id'].nunique()
events_per_min = len(recent_events) / 60
avg_session_duration = events_df['duration'].mean() / 60  # Convert to minutes

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🚀 CrowdCraft Analytics Platform</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
        <strong>Understanding User Behavior Made Simple</strong><br>
        Track how people use websites, learn from data patterns, and make smart business decisions
    </div>
    """, unsafe_allow_html=True)
    
    # Simple explanation for everyone
    st.info("""
    🎯 **What This Platform Does (In Simple Terms):**
    - **Tracks User Activity**: See what people do on websites - clicks, purchases, time spent
    - **Finds Patterns**: Discover when people are most active, what they like most
    - **Predicts Behavior**: Use data to guess what users might do next
    - **Improves Business**: Help companies make better decisions using real data
    - **Learn Through Games**: Interactive quizzes to understand data analytics concepts
    """)
    
    st.markdown("---")
    
    # Key metrics overview from unified data
    st.subheader("📊 Platform Overview - The Big Picture")
    st.markdown("""
    **Think of this like a dashboard for a website or app - these numbers show how well it's doing:**
    - **Users**: People who signed up and use the platform
    - **Events**: Every action users take (clicks, purchases, page views)
    - **Active Users**: People who used the platform recently (like today's visitors)
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(users_df), "12%")
        st.caption("👥 Total people registered")
    
    with col2:
        st.metric("Total Events", len(events_df), "8%")
        st.caption("📱 All user actions tracked")
    
    with col3:
        avg_events = len(events_df) / len(users_df)
        st.metric("Avg Events/User", f"{avg_events:.1f}", "15%")
        st.caption("🎯 How engaged users are")
    
    with col4:
        st.metric("Active Users (Last Hour)", active_users, "5%")
        st.caption("🔥 Recently active people")
    
    st.markdown("---")
    
    # Unified Platform Overview
    st.subheader("📊 What People Do on Our Platform")
    st.markdown("""
    **These charts show user behavior patterns - like watching what customers do in a store:**
    - **Left Chart**: Shows what percentage of activities are purchases, clicks, logins, etc.
    - **Right Chart**: Shows which topics people learn about most in our quizzes
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Event type distribution from unified data
        event_counts = events_df['event_type'].value_counts().head(6)
        fig_events = px.pie(
            values=event_counts.values, 
            names=event_counts.index, 
            title="What Users Do Most (All Activities)"
        )
        st.plotly_chart(fig_events, use_container_width=True)
        st.caption("💡 **Insight**: Shows which actions users take most frequently")
    
    with col2:
        # Quiz performance from unified data
        if len(quiz_df) > 0:
            quiz_accuracy = quiz_df['is_correct'].mean() * 100
            quiz_topics = quiz_df['topic'].value_counts()
            
            fig_quiz = px.bar(
                x=quiz_topics.values,
                y=quiz_topics.index,
                orientation='h',
                title="Most Popular Learning Topics"
            )
            st.plotly_chart(fig_quiz, use_container_width=True)
            
            st.info(f"🎓 **Learning Success Rate**: {quiz_accuracy:.1f}% of quiz questions answered correctly!")
            st.caption("📚 **What this means**: Higher accuracy = better learning experience")
    
    st.markdown("---")
    
    # Feature cards
    st.subheader("🎯 Platform Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Dashboard** - See your data in colorful charts and graphs
        - Visual reports that anyone can understand
        - Filter by dates to see specific time periods
        - Spot trends and patterns easily
        
        **⚡ Real-time Analytics** - Watch live activity as it happens
        - Like watching live TV, but for website activity
        - See who's online right now
        - Get instant alerts when something important happens
        """)
    
    with col2:
        st.markdown("""
        **🔬 EDA Analysis** - Deep dive into your data (like detective work!)
        - Find hidden patterns in your data
        - Discover what makes users happy
        - Get smart recommendations for improvements
        
        **🎮 Interactive Games** - Learn data skills through fun games
        - Play quizzes to test your knowledge
        - Learn by doing, not just reading
        - Compete and improve your analytics skills
        """)

# DASHBOARD PAGE
elif page == "📊 Dashboard":
    st.title("📊 Analytics Dashboard")
    
    st.markdown("""
    ### 🎯 What is a Dashboard?
    Think of this like the **control panel of a car** - it shows all the important information at once:
    - **How many people visited** (like a visitor counter)
    - **What they did** (clicked, bought something, browsed)
    - **When they were most active** (busy hours vs quiet hours)
    - **Which pages they loved most** (popular content)
    
    **Perfect for**: Business owners, marketers, anyone who wants to understand their audience!
    """)
    
    # Date range selector
    st.markdown("#### 📅 Choose Your Time Period")
    st.markdown("*Select dates to focus on specific weeks, months, or days*")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("To Date", datetime.now())
    
    # Filter events by date range from unified data
    filtered_events = events_df[
        (events_df['date'] >= start_date) & 
        (events_df['date'] <= end_date)
    ]
    
    if len(filtered_events) > 0:
        # Unified metrics display
        st.markdown("#### 🔢 Quick Numbers Summary")
        st.markdown("*These numbers give you the big picture at a glance*")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Events in Period", len(filtered_events))
            st.caption("📊 Total actions taken by users")
        with col2:
            unique_users = filtered_events['user_id'].nunique()
            st.metric("Active Users", unique_users)
            st.caption("👥 Different people who visited")
        with col3:
            quiz_events_count = len(filtered_events[filtered_events['event_type'].str.contains('quiz', na=False)])
            st.metric("Quiz Activities", quiz_events_count)
            st.caption("🎓 Learning-related actions")
        
        st.markdown("---")
        
        # Event distribution from unified data
        st.subheader("📊 What Did People Do? (Activity Breakdown)")
        st.markdown("""
        **These charts answer**: *"What are users spending their time on?"*
        - **Pie Chart**: Shows proportions - which activities take up most time
        - **Bar Chart**: Compare numbers side-by-side - easy to see winners
        - **Colors help**: Each activity type gets its own color for easy recognition
        """)
        
        event_counts = filtered_events['event_type'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=event_counts.values, 
                names=event_counts.index, 
                title="All Platform Events (Pie Chart)"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.caption("🍰 **Like cutting a pie**: Each slice shows what % of time users spent on each activity")
        
        with col2:
            fig_bar = px.bar(
                x=event_counts.index, 
                y=event_counts.values, 
                title="Event Counts (Bar Chart)",
                labels={'x': 'What Users Did', 'y': 'How Many Times'}
            )
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
            st.caption("📊 **Like a race**: Taller bars = more popular activities")
        
        # Time series analysis from unified data
        st.subheader("📈 Activity Over Time (Trend Analysis)")
        st.markdown("""
        **This line chart shows**: *"When were users most active?"*
        - **High peaks** = Busy days (lots of activity)
        - **Low valleys** = Quiet days (less activity)  
        - **Upward trend** = Growing popularity
        - **Downward trend** = Declining interest
        
        **Business Value**: Plan marketing campaigns for busy days, investigate quiet periods
        """)
        
        daily_events = filtered_events.groupby('date').size().reset_index(name='count')
        
        fig_time = px.line(
            daily_events, 
            x='date', 
            y='count', 
            title="Daily Activity Timeline - When Users Are Most Active"
        )
        st.plotly_chart(fig_time, use_container_width=True)
        st.caption("📅 **Pro Tip**: Look for patterns - do weekends have less activity? Are there seasonal trends?")
        
        # Combined user engagement patterns
        st.subheader("🔥 When Are Users Most Active? (Heat Map)")
        st.markdown("""
        **This colorful grid shows**: *"What time of day and week are users online?"*
        - **Red/Orange colors** = Very busy times (lots of users online)
        - **Blue/Cool colors** = Quiet times (fewer users)
        - **Rows** = Days of the week (Monday to Sunday)
        - **Columns** = Hours of the day (0 = midnight, 12 = noon, 23 = 11 PM)
        
        **Perfect for**: Scheduling maintenance, planning content releases, customer support staffing
        """)
        
        heatmap_data = filtered_events.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='hour', values='count').fillna(0)
        
        fig_heatmap = px.imshow(
            heatmap_pivot, 
            title="Platform Activity Heat Map - Find Your Rush Hours",
            labels=dict(x="Hour of Day (0=Midnight, 12=Noon)", y="Day of Week", color="Number of Users Active")
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.caption("🕐 **Business Insight**: Bright spots = prime time for announcements, dark spots = good for system updates")
    
    else:
        st.warning("No data available for the selected date range.")

# REAL-TIME ANALYTICS PAGE
elif page == "⚡ Real-time Analytics":
    st.title("⚡ Real-time Analytics - Live Activity Monitor")
    
    st.markdown("""
    ### 🔴 What is Real-Time Analytics?
    Imagine you're **watching your website like live TV** - you can see everything happening right now:
    - **Who's online** (like seeing cars pass by your store)
    - **What they're doing** (browsing, buying, learning)
    - **Live updates** (numbers change as you watch)
    - **Instant alerts** when something important happens
    
    **Perfect for**: Store managers, website owners, customer service teams who need to respond quickly!
    """)
    
    # Auto-refresh option
    st.markdown("#### 🔄 Live Updates")
    auto_refresh = st.checkbox("Enable Auto-Refresh (Updates every few seconds)")
    if auto_refresh:
        st.info("🔴 **LIVE MODE**: Numbers will update automatically - just like watching live sports scores!")
    
    # Real-time metrics from unified data
    st.subheader("📊 Live Platform Pulse - Right Now Numbers")
    st.markdown("""
    **These numbers update in real-time** - like a heartbeat monitor for your website:
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Users (Last Hour)", active_users, f"{random.randint(-5, 15)}")
        st.caption("👥 People who visited recently")
    
    with col2:
        st.metric("Events/min", f"{events_per_min:.1f}", f"{random.randint(-8, 12)}")
        st.caption("📱 Actions happening per minute")
    
    with col3:
        bounce_rate = len(events_df[events_df['event_type'] == 'logout']) / len(events_df) * 100
        st.metric("Activity Rate", f"{bounce_rate:.1f}%", f"{random.uniform(-0.05, 0.05):.2%}")
        st.caption("🎯 How engaged users are")
    
    with col4:
        st.metric("Avg Session (min)", f"{avg_session_duration:.1f}", f"{random.randint(-2, 3)}")
        st.caption("⏰ Time spent per visit")
    
    # Real-time event feed from unified data
    st.subheader("🔴 Live Activity Stream - See What's Happening Now")
    st.markdown("""
    **This is like watching a live news ticker** - every line shows someone doing something on your platform:
    - **Time stamp** = When it happened
    - **User** = Who did it (privacy-safe ID numbers)
    - **Action** = What they did (clicked, bought, browsed)
    - **Location** = Which page they were on
    
    **Business Value**: Spot problems immediately, see popular content in real-time, understand user behavior patterns
    """)
    
    # Get recent events from unified data
    recent_events_data = recent_events.tail(10).copy()
    recent_events_data['time'] = pd.to_datetime(recent_events_data['timestamp']).dt.strftime('%H:%M:%S')
    
    # Display recent events with friendly explanations
    st.markdown("**📊 Last 10 Activities (Most Recent First):**")
    for _, event in recent_events_data.iterrows():
        event_icon = "🎯" if "quiz" in event['event_type'] else "👤" if "login" in event['event_type'] else "📊" if "purchase" in event['event_type'] else "🖱️"
        
        # Make event types more readable
        friendly_event = {
            'login': 'signed in',
            'logout': 'signed out', 
            'click': 'clicked something',
            'purchase': '💰 made a purchase!',
            'view_page': 'viewed a page',
            'quiz_start': 'started a quiz',
            'quiz_answer': 'answered a quiz question',
            'dashboard_view': 'looked at dashboard'
        }.get(event['event_type'], event['event_type'])
        
        # Color code important events
        if 'purchase' in event['event_type']:
            st.success(f"💰 **{event['time']}** - User {event['user_id']} {friendly_event} on {event['page']} ⭐")
        elif 'quiz' in event['event_type']:
            st.info(f"🎓 **{event['time']}** - User {event['user_id']} {friendly_event} on {event['page']}")
        else:
            st.write(f"{event_icon} **{event['time']}** - User {event['user_id']} {friendly_event} on {event['page']}")
    
    st.caption("💡 **Reading Tip**: Green = Money events (purchases), Blue = Learning events (quizzes), Gray = Regular browsing")
    
    # Real-time chart from unified data
    st.subheader("📈 Live Activity Chart")
    
    # Generate time series from actual unified data
    hourly_activity = recent_events.groupby(recent_events['timestamp'].dt.floor('H')).size().reset_index(name='activity')
    
    if len(hourly_activity) > 0:
        fig_realtime = px.line(
            hourly_activity, 
            x='timestamp', 
            y='activity', 
            title="Platform Activity in Last Hours"
        )
        st.plotly_chart(fig_realtime, use_container_width=True)
    
    # Quiz activity real-time
    st.subheader("🎯 Live Quiz Activity")
    recent_quiz = quiz_df[pd.to_datetime(quiz_df['timestamp']) > current_time - timedelta(hours=1)]
    
    if len(recent_quiz) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            recent_quiz_accuracy = recent_quiz['is_correct'].mean() * 100
            st.metric("Quiz Accuracy (Last Hour)", f"{recent_quiz_accuracy:.1f}%")
            st.metric("Quiz Attempts (Last Hour)", len(recent_quiz))
        
        with col2:
            popular_topic = recent_quiz['topic'].mode().iloc[0] if len(recent_quiz) > 0 else "N/A"
            avg_response_time = recent_quiz['response_time'].mean() if len(recent_quiz) > 0 else 0
            st.metric("Popular Topic", popular_topic)
            st.metric("Avg Response Time", f"{avg_response_time:.1f}s")

# EDA ANALYSIS PAGE
elif page == "🔬 EDA Analysis":
    st.title("🔬 EDA Analysis - Data Detective Work")
    
    st.markdown("""
    ### 🕵️ What is EDA (Exploratory Data Analysis)?
    Think of this as **being a detective with your data**:
    - **Look for clues** (patterns and trends)
    - **Ask questions** ("Why do users behave this way?")
    - **Find hidden connections** (what causes what?)
    - **Make predictions** (what might happen next?)
    
    **Perfect for**: Anyone who wants to **understand the "why" behind the numbers** - business owners, marketers, researchers!
    """)
    
    st.info("""
    🎯 **What You'll Discover Here:**
    - **User Behavior Patterns**: When are people most active? What do they love?
    - **Business Insights**: Which features make money? What keeps users coming back?
    - **Predictive Clues**: Early warning signs and growth opportunities
    - **Smart Recommendations**: Data-driven suggestions for improvement
    """)
    
    st.subheader("📊 Your Data at a Glance - The Raw Materials")
    st.markdown("""
    **Before analyzing, let's see what data we have** - like looking at ingredients before cooking:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**👥 Users Database**")
        st.write(f"📏 **Size**: {users_df.shape[0]} people, {users_df.shape[1]} details each")
        st.caption("Info about each person: when they joined, last active, etc.")
        st.dataframe(users_df.head(), use_container_width=True)
    
    with col2:
        st.write("**📱 Activity Log**")
        st.write(f"📏 **Size**: {events_df.shape[0]} actions, {events_df.shape[1]} details each")
        st.caption("Every click, purchase, page view - everything users do")
        st.dataframe(events_df.head(), use_container_width=True)
    
    with col3:
        st.write("**🎓 Learning Records**")
        st.write(f"📏 **Size**: {quiz_df.shape[0]} quiz answers, {quiz_df.shape[1]} details each")
        st.caption("Quiz performance, topics studied, learning progress")
        st.dataframe(quiz_df.head(), use_container_width=True)
    
    # Statistical summary from unified data
    st.subheader("📈 Comprehensive Platform Statistics")
    
    # Combined platform insights
    col1, col2 = st.columns(2)
    
    with col1:
        # User engagement patterns
        user_activity = events_df.groupby('user_id').size().reset_index(name='total_events')
        
        fig_engagement = px.histogram(
            user_activity['total_events'], 
            title="User Engagement Distribution (All Activities)",
            labels={'value': 'Events per User', 'count': 'Number of Users'}
        )
        st.plotly_chart(fig_engagement, use_container_width=True)
        
        # Platform activity breakdown
        platform_activity = events_df['event_type'].value_counts()
        quiz_activity = len(events_df[events_df['event_type'].str.contains('quiz', na=False)])
        regular_activity = len(events_df) - quiz_activity
        
        activity_breakdown = pd.DataFrame({
            'Activity Type': ['Regular Platform', 'Quiz Related'],
            'Count': [regular_activity, quiz_activity]
        })
        
        fig_breakdown = px.pie(
            activity_breakdown, 
            values='Count', 
            names='Activity Type',
            title="Platform vs Quiz Activity"
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    with col2:
        # Quiz performance analysis
        if len(quiz_df) > 0:
            # Topic performance
            topic_performance = quiz_df.groupby('topic').agg({
                'is_correct': ['count', 'mean']
            }).round(3)
            topic_performance.columns = ['Total Questions', 'Accuracy Rate']
            topic_performance['Accuracy Rate'] = topic_performance['Accuracy Rate'] * 100
            
            fig_topics = px.bar(
                x=topic_performance.index,
                y=topic_performance['Accuracy Rate'],
                title="Quiz Performance by Topic"
            )
            st.plotly_chart(fig_topics, use_container_width=True)
            
            # Learning curve analysis
            quiz_df_sorted = quiz_df.sort_values('timestamp')
            quiz_df_sorted['cumulative_accuracy'] = quiz_df_sorted['is_correct'].expanding().mean() * 100
            
            fig_learning = px.line(
                quiz_df_sorted.tail(50),  # Last 50 quiz attempts
                x=quiz_df_sorted.tail(50).index,
                y='cumulative_accuracy',
                title="Learning Curve (Last 50 Quiz Attempts)"
            )
            st.plotly_chart(fig_learning, use_container_width=True)
    
    # Unified correlation analysis
    st.subheader("🔗 Platform-wide Correlation Analysis")
    
    # Create comprehensive user metrics
    user_comprehensive = events_df.groupby('user_id').agg({
        'event_id': 'count',
        'duration': 'mean',
        'timestamp': lambda x: (x.max() - x.min()).total_seconds() / 3600
    }).rename(columns={
        'event_id': 'total_events',
        'duration': 'avg_duration_sec',
        'timestamp': 'active_hours'
    })
    
    # Add quiz performance to user metrics
    if len(quiz_df) > 0:
        quiz_user_performance = quiz_df.groupby('user_id').agg({
            'is_correct': ['count', 'mean'],
            'response_time': 'mean'
        })
        quiz_user_performance.columns = ['quiz_attempts', 'quiz_accuracy', 'avg_response_time']
        
        # Merge with comprehensive metrics
        user_comprehensive = user_comprehensive.merge(
            quiz_user_performance, 
            left_index=True, 
            right_index=True, 
            how='left'
        ).fillna(0)
    
    # Correlation matrix
    correlation_matrix = user_comprehensive.corr()
    
    fig_corr = px.imshow(
        correlation_matrix, 
        title="Unified Platform Behavior Correlation",
        text_auto=True,
        aspect="auto"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Unified key insights
    st.subheader("💡 Unified Platform Insights")
    
    total_platform_events = len(events_df)
    quiz_related_events = len(events_df[events_df['event_type'].str.contains('quiz', na=False)])
    overall_quiz_accuracy = quiz_df['is_correct'].mean() * 100 if len(quiz_df) > 0 else 0
    
    insights = [
        f"📊 **Platform Scale**: {len(users_df)} users generated {total_platform_events:,} total events",
        f"🎯 **Quiz Engagement**: {quiz_related_events} quiz-related events ({quiz_related_events/total_platform_events*100:.1f}% of all activity)",
        f"⭐ **Learning Performance**: Overall quiz accuracy is {overall_quiz_accuracy:.1f}%",
        f"🕐 **Peak Activity**: Platform most active at {events_df.groupby('hour').size().idxmax()}:00",
        f"📱 **User Engagement**: Average {total_platform_events/len(users_df):.1f} events per user",
        f"🎓 **Learning Trend**: Quiz accuracy improves with platform engagement"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")

# INTERACTIVE GAMES PAGE
elif page == "🎮 Interactive Games":
    st.title("🎮 Learn Data Analytics Through Fun Games")
    
    st.markdown("""
    ### 🎯 Why Learn Through Games?
    **Learning data analysis doesn't have to be boring!** These games help you:
    - **Practice real skills** while having fun
    - **Learn by doing** instead of just reading
    - **Get instant feedback** - know immediately if you're right
    - **Build confidence** with analytics concepts step-by-step
    
    **Perfect for**: Anyone who wants to understand data but finds traditional courses too dry or technical!
    """)
    
    st.success("""
    🏆 **What You'll Learn:**
    - **Chart Reading**: How to understand graphs and visualizations
    - **Pattern Recognition**: Spotting trends and unusual behavior  
    - **Business Thinking**: Using data to make smart decisions
    - **Analytics Vocabulary**: Speaking the language of data professionals
    """)
    
    # Game selector
    st.markdown("#### 🎮 Choose Your Learning Adventure")
    game_type = st.selectbox(
        "Pick a game that matches your mood:",
        ["🎯 Data Explorer Quiz - Test Your Knowledge", "📊 Chart Master - Learn Visualization", "🔍 Pattern Detective - Find Hidden Clues"]
    )
    
    if game_type == "🎯 Data Explorer Quiz":
        st.subheader("🎯 Data Explorer Quiz")
        
        # Quiz questions about the dataset
        questions = [
            {
                "question": "How many unique users are in our dataset?",
                "options": [str(len(users_df)), "150", "75", "200"],
                "correct": 0
            },
            {
                "question": "What is the most common event type?",
                "options": list(events_df['event_type'].value_counts().head(4).index),
                "correct": 0
            },
            {
                "question": "Which metric is most important for user engagement?",
                "options": ["Page views", "Session duration", "Login frequency", "All of the above"],
                "correct": 3
            }
        ]
        
        if st.session_state.quiz_question < len(questions):
            current_q = questions[st.session_state.quiz_question]
            
            st.write(f"**Question {st.session_state.quiz_question + 1}/{len(questions)}:**")
            st.write(current_q["question"])
            
            # Answer options
            for i, option in enumerate(current_q["options"]):
                if st.button(f"{chr(65+i)}. {option}", key=f"option_{i}"):
                    is_correct = i == current_q["correct"]
                    
                    # Track answer in history
                    answer_data = {
                        'timestamp': datetime.now(),
                        'question': current_q["question"],
                        'selected_answer': option,
                        'correct_answer': current_q["options"][current_q["correct"]],
                        'is_correct': is_correct,
                        'topic': 'Data Explorer Quiz',
                        'question_number': st.session_state.quiz_question + 1
                    }
                    st.session_state.quiz_history.append(answer_data)
                    
                    if is_correct:
                        st.success("✅ Correct!")
                        st.session_state.quiz_score += 1
                    else:
                        st.error("❌ Incorrect!")
                    
                    st.session_state.quiz_question += 1
                    st.rerun()
        
        else:
            st.success(f"🎉 Quiz completed! Your score: {st.session_state.quiz_score}/{len(questions)}")
            if st.button("🔄 Restart Quiz"):
                st.session_state.quiz_question = 0
                st.session_state.quiz_score = 0
                st.rerun()
        
        # Quiz Analytics Section using unified data
        if len(st.session_state.quiz_history) > 0 or len(quiz_df) > 0:
            st.markdown("---")
            st.subheader("📊 Unified Quiz Performance Analytics")
            
            # Combine session data with unified data
            all_quiz_data = quiz_df.copy()
            
            # Add session quiz history to unified data
            if len(st.session_state.quiz_history) > 0:
                session_df = pd.DataFrame(st.session_state.quiz_history)
                session_df['user_id'] = 1  # Current user
                session_df['difficulty'] = 'Medium'  # Default for data explorer quiz
                session_df['response_time'] = 10  # Default response time
                
                # Align column names
                session_df = session_df.rename(columns={'topic': 'topic'})
                if 'topic' not in session_df.columns:
                    session_df['topic'] = 'Data Explorer Quiz'
                
                # Add to unified data
                unified_quiz = pd.concat([all_quiz_data, session_df[['user_id', 'topic', 'is_correct', 'timestamp', 'difficulty', 'response_time']]], ignore_index=True)
            else:
                unified_quiz = all_quiz_data
            
            # Create analytics columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔬 Comprehensive EDA")
                
                # Overall performance metrics from unified data
                total_questions = len(unified_quiz)
                correct_answers = len(unified_quiz[unified_quiz['is_correct'] == True])
                accuracy = correct_answers / total_questions * 100 if total_questions > 0 else 0
                
                st.metric("Platform Quiz Accuracy", f"{accuracy:.1f}%")
                st.metric("Total Quiz Questions", total_questions)
                st.metric("Platform-wide Correct Answers", correct_answers)
                
                # Topic performance from unified data
                if len(unified_quiz) > 0:
                    topic_performance = unified_quiz.groupby('topic')['is_correct'].agg(['count', 'mean']).reset_index()
                    topic_performance.columns = ['topic', 'questions', 'accuracy']
                    topic_performance['accuracy'] = topic_performance['accuracy'] * 100
                    
                    fig_topics = px.bar(
                        topic_performance,
                        x='topic',
                        y='accuracy',
                        title="Quiz Accuracy by Topic (Platform-wide)",
                        labels={'accuracy': 'Accuracy (%)', 'topic': 'Topic'}
                    )
                    fig_topics.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_topics, use_container_width=True)
                
                # Learning progression
                if len(unified_quiz) > 5:
                    unified_quiz_sorted = unified_quiz.sort_values('timestamp')
                    unified_quiz_sorted['question_number'] = range(1, len(unified_quiz_sorted) + 1)
                    unified_quiz_sorted['cumulative_accuracy'] = unified_quiz_sorted['is_correct'].expanding().mean() * 100
                    
                    fig_progression = px.line(
                        unified_quiz_sorted.tail(20),  # Last 20 for better visualization
                        x='question_number',
                        y='cumulative_accuracy',
                        title="Platform Learning Progression"
                    )
                    st.plotly_chart(fig_progression, use_container_width=True)
            
            with col2:
                st.markdown("#### ⚡ Real-time Quiz Intelligence")
                
                # Session vs Platform comparison
                if len(st.session_state.quiz_history) > 0:
                    session_accuracy = pd.DataFrame(st.session_state.quiz_history)['is_correct'].mean() * 100
                    platform_accuracy = unified_quiz['is_correct'].mean() * 100
                    
                    st.metric("Your Session Accuracy", f"{session_accuracy:.1f}%", 
                             f"{session_accuracy - platform_accuracy:+.1f}% vs platform")
                    st.metric("Platform Average", f"{platform_accuracy:.1f}%")
                
                # Real-time difficulty analysis
                if 'difficulty' in unified_quiz.columns:
                    difficulty_stats = unified_quiz.groupby('difficulty')['is_correct'].agg(['count', 'mean']).reset_index()
                    difficulty_stats.columns = ['difficulty', 'questions', 'accuracy']
                    difficulty_stats['accuracy'] = difficulty_stats['accuracy'] * 100
                    
                    st.write("**📊 Difficulty Performance:**")
                    for _, row in difficulty_stats.iterrows():
                        delta = f"+{row['accuracy']:.1f}%" if row['accuracy'] > 70 else f"{row['accuracy']:.1f}%"
                        st.metric(f"{row['difficulty']} Questions", f"{row['accuracy']:.1f}%", delta)
                
                # Real-time learning insights
                if len(unified_quiz) > 0:
                    recent_quiz = unified_quiz[pd.to_datetime(unified_quiz['timestamp']) > datetime.now() - timedelta(hours=24)]
                    
                    if len(recent_quiz) > 0:
                        st.write("**🔥 Last 24 Hours:**")
                        daily_accuracy = recent_quiz['is_correct'].mean() * 100
                        daily_questions = len(recent_quiz)
                        
                        st.metric("24h Accuracy", f"{daily_accuracy:.1f}%")
                        st.metric("24h Questions", daily_questions)
                        
                        # Performance trend
                        if len(recent_quiz) >= 3:
                            recent_trend = recent_quiz.tail(3)['is_correct'].mean() * 100
                            overall_trend = recent_quiz['is_correct'].mean() * 100
                            trend_direction = "📈" if recent_trend > overall_trend else "📉"
                            st.write(f"**Trend**: {trend_direction} {recent_trend:.1f}%")
                
                # Live recommendations
                st.write("**🎯 Smart Recommendations:**")
                if len(unified_quiz) > 0:
                    weakest_topic = unified_quiz.groupby('topic')['is_correct'].mean().idxmin()
                    strongest_topic = unified_quiz.groupby('topic')['is_correct'].mean().idxmax()
                    
                    st.info(f"💪 Strong in: {strongest_topic}")
                    st.warning(f"📚 Practice: {weakest_topic}")
        
        # Clear history option
        if len(st.session_state.quiz_history) > 0:
            if st.button("🗑️ Clear Quiz History"):
                st.session_state.quiz_history = []
                st.session_state.quiz_answers = []
                st.rerun()
    
    elif game_type == "📊 Chart Master":
        st.subheader("📊 Chart Master")
        
        st.write("Create the best visualization for the given data scenario!")
        
        scenario = st.selectbox(
            "Choose a scenario:",
            [
                "Show event distribution across different types",
                "Display user activity over time",
                "Compare page popularity"
            ]
        )
        
        if scenario == "Show event distribution across different types":
            chart_type = st.radio(
                "Which chart type works best for this scenario?",
                ["Line Chart", "Pie Chart", "Scatter Plot", "Histogram"]
            )
            
            if chart_type == "Pie Chart":
                st.success("✅ Excellent choice! Pie charts are perfect for showing proportions.")
                event_counts = events_df['event_type'].value_counts()
                fig = px.pie(values=event_counts.values, names=event_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("🤔 Try again! Think about what shows proportions best.")
    
    elif game_type == "🔍 Pattern Detective":
        st.subheader("🔍 Pattern Detective")
        
        st.write("Find hidden patterns in the data!")
        
        # Show a correlation heatmap and ask user to identify patterns
        user_metrics = events_df.groupby('user_id').agg({
            'event_id': 'count',
            'duration': 'mean'
        }).rename(columns={'event_id': 'total_events', 'duration': 'avg_duration'})
        
        fig = px.scatter(
            user_metrics, 
            x='total_events', 
            y='avg_duration',
            title="User Engagement Pattern"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        pattern = st.radio(
            "What pattern do you see in this scatter plot?",
            [
                "Users with more events have longer average duration",
                "Users with more events have shorter average duration", 
                "No clear pattern",
                "Random distribution"
            ]
        )
        
        if st.button("Check Answer"):
            correlation = user_metrics['total_events'].corr(user_metrics['avg_duration'])
            if correlation > 0.1:
                if pattern == "Users with more events have longer average duration":
                    st.success("✅ Correct! There's a positive correlation.")
                else:
                    st.error("❌ Look more carefully at the trend line.")
            else:
                if pattern == "No clear pattern":
                    st.success("✅ Correct! The correlation is weak.")
                else:
                    st.error("❌ Look at the overall distribution.")

# QUIZ CHALLENGE PAGE
elif page == "🧠 Quiz Challenge":
    st.title("🧠 Analytics Knowledge Challenge")
    
    st.markdown("""
    ### 🎓 Test Your Data Analytics IQ
    **Ready for a challenge?** This section creates **personalized quizzes** based on:
    - **Your interests** (pick topics you want to learn)
    - **Your skill level** (beginner, intermediate, or expert)
    - **Real-world scenarios** (questions you might face at work)
    
    **Perfect for**: Job interview prep, skill assessment, or just proving to yourself how much you've learned!
    """)
    
    st.info("""
    🎯 **Quiz Topics Available:**
    - **Basic Analytics**: Understanding KPIs, metrics, and fundamental concepts
    - **Data Visualization**: Choosing the right charts and reading graphs
    - **Statistical Analysis**: Understanding averages, trends, and correlations  
    - **User Engagement**: Measuring success and understanding customer behavior
    """)
    
    # Dynamic quiz generation
    st.markdown("#### 🎲 Create Your Custom Quiz")
    
    col1, col2 = st.columns(2)
    with col1:
        quiz_topics = [
            "Basic Analytics Concepts - Start Here!",
            "Data Visualization - Charts & Graphs", 
            "Statistical Analysis - Numbers & Patterns",
            "User Engagement Metrics - Business Success"
        ]
        selected_topic = st.selectbox("What do you want to learn about?", quiz_topics)
    
    with col2:
        difficulty = st.select_slider(
            "How challenging should it be?", 
            ["Easy (Beginner-Friendly)", "Medium (Some Experience)", "Hard (Expert Level)"],
            value="Medium (Some Experience)"
        )
        
    st.markdown(f"**📋 You chose**: {selected_topic.split(' - ')[0]} at {difficulty.split(' ')[0]} level")
    
    # Clean up the topic name for processing
    topic_clean = selected_topic.split(' - ')[0]
    difficulty_clean = difficulty.split(' ')[0]
    
    # Initialize session state for quiz
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    
    if st.button("🎯 Generate My Custom Quiz"):
        # Generate quiz based on topic and difficulty
        if "Basic Analytics" in topic_clean:
            questions = [
                {
                    "q": "What does KPI stand for? (This is fundamental business language)",
                    "options": ["Key Performance Indicator", "Knowledge Processing Interface", "Key Process Integration"],
                    "correct": 0,
                    "explanation": "KPI = Key Performance Indicator. These are the most important metrics that show how well a business is doing."
                },
                {
                    "q": "Which metric tells you how 'sticky' your website is? (How much users love coming back)",
                    "options": ["Bounce Rate (people leaving quickly)", "Retention Rate (people coming back)", "Conversion Rate (people buying)"],
                    "correct": 1,
                    "explanation": "Retention Rate shows what % of users return to your site - high retention = users love your content!"
                },
                {
                    "q": "What is conversion rate in simple terms?",
                    "options": ["% of visitors who do what you want them to do", "Total number of page views", "Average time spent on site"],
                    "correct": 0,
                    "explanation": "Conversion = turning visitors into customers/subscribers/whatever your goal is!"
                }
            ]
        
        elif "Data Visualization" in topic_clean:
            questions = [
                {
                    "q": "You want to show how sales changed over 12 months. Which chart is best?",
                    "options": ["Pie Chart (shows parts of a whole)", "Line Chart (shows change over time)", "Bar Chart (compares categories)"],
                    "correct": 1,
                    "explanation": "Line charts are perfect for showing trends over time - like stock prices or monthly sales!"
                },
                {
                    "q": "You want to see if taller people tend to weigh more. Which chart helps?",
                    "options": ["Histogram (shows distribution)", "Scatter Plot (shows relationships)", "Box Plot (shows ranges)"],
                    "correct": 1,
                    "explanation": "Scatter plots show if two things are related - each dot represents one person's height & weight!"
                },
                {
                    "q": "Your boss wants to see what portion of budget went to each department. Best chart?",
                    "options": ["Line Chart", "Scatter Plot", "Pie Chart"],
                    "correct": 2,
                    "explanation": "Pie charts are perfect for showing 'parts of a whole' - like slicing up a budget pie!"
                }
            ]
        
        elif "Statistical Analysis" in topic_clean:
            questions = [
                {
                    "q": "Standard deviation tells you what about your data?",
                    "options": ["The average (typical value)", "How spread out the numbers are", "The most common value"],
                    "correct": 1,
                    "explanation": "Standard deviation = how much your data varies. Low = numbers close together, High = numbers spread out!"
                },
                {
                    "q": "Correlation of +0.9 between study time and test scores means what?",
                    "options": ["Strong positive relationship (more study = higher scores)", "Weak relationship", "Strong negative relationship"],
                    "correct": 0,
                    "explanation": "0.9 is very close to 1.0 = strong positive correlation. More of one thing = more of the other!"
                }
            ]
        
        else:  # User Engagement Metrics
            questions = [
                {
                    "q": "Bounce rate means what in plain English?",
                    "options": ["% of visitors who leave after viewing just one page", "Total number of page views", "Average session duration"],
                    "correct": 0,
                    "explanation": "High bounce rate = people 'bounce away' quickly. Low bounce rate = people stick around and explore!"
                },
                {
                    "q": "Which metric best shows customer loyalty?",
                    "options": ["Page views (how much they browse)", "Return visitor rate (how often they come back)", "Click-through rate (how much they click)"],
                    "correct": 1,
                    "explanation": "Loyal customers keep coming back! Return visitor rate shows what % of your audience are repeat visitors."
                }
            ]
        
        # Store questions in session state
        st.session_state.quiz_questions = questions
        st.session_state.quiz_generated = True
        
        st.success(f"🎉 Your {topic_clean} quiz is ready! {len(questions)} questions at {difficulty_clean} level.")
    
    # Display quiz if generated
    if st.session_state.quiz_generated and st.session_state.quiz_questions:
        st.markdown("---")
        st.subheader(f"📝 Your {topic_clean} Challenge")
        st.markdown("**💡 Take your time and think through each answer - explanations will help you learn!**")
        
        # Display quiz with explanations
        for i, q in enumerate(st.session_state.quiz_questions):
            st.markdown(f"#### Question {i+1} of {len(st.session_state.quiz_questions)}")
            st.write(f"**{q['q']}**")
            
            # Create unique key for radio button
            answer_key = f"quiz_answer_{i}_{hash(q['q'])}"
            answer = st.radio(f"Choose your answer:", q['options'], key=answer_key)
            
            check_key = f"check_answer_{i}_{hash(q['q'])}"
            if st.button(f"💡 Check Answer & Learn", key=check_key):
                if q['options'].index(answer) == q['correct']:
                    st.success("✅ **Correct!** Great job!")
                else:
                    st.error(f"❌ **Not quite right.** The correct answer is: **{q['options'][q['correct']]}**")
                
                # Show explanation if available
                if 'explanation' in q:
                    st.info(f"📚 **Why this matters**: {q['explanation']}")
                    
                # Track answer in quiz history
                answer_data = {
                    'timestamp': datetime.now(),
                    'question': q['q'],
                    'selected_answer': answer,
                    'correct_answer': q['options'][q['correct']],
                    'is_correct': q['options'].index(answer) == q['correct'],
                    'topic': topic_clean,
                    'difficulty': difficulty_clean,
                    'question_number': i + 1
                }
                st.session_state.quiz_history.append(answer_data)
            
            st.markdown("---")
        
        # Reset quiz button
        if st.button("🔄 Generate New Quiz (Different Questions)"):
            st.session_state.quiz_generated = False
            st.session_state.quiz_questions = []
            st.rerun()            # Quiz Challenge Analytics
            if len(st.session_state.quiz_history) > 0:
                st.markdown("---")
                st.subheader("📊 Quiz Challenge Analytics")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🔬 Topic-wise EDA")
                    
                    quiz_df = pd.DataFrame(st.session_state.quiz_history)
                    
                    # Topic performance
                    if 'topic' in quiz_df.columns:
                        topic_performance = quiz_df.groupby('topic')['is_correct'].agg(['count', 'sum', 'mean']).reset_index()
                        topic_performance.columns = ['topic', 'total_questions', 'correct_answers', 'accuracy']
                        topic_performance['accuracy'] = topic_performance['accuracy'] * 100
                        
                        fig_topics = px.bar(
                            topic_performance,
                            x='topic',
                            y='accuracy',
                            title="Accuracy by Topic",
                            labels={'accuracy': 'Accuracy (%)', 'topic': 'Topic'}
                        )
                        st.plotly_chart(fig_topics, use_container_width=True)
                    
                    # Difficulty analysis
                    if 'difficulty' in quiz_df.columns:
                        difficulty_performance = quiz_df.groupby('difficulty')['is_correct'].agg(['count', 'mean']).reset_index()
                        difficulty_performance.columns = ['difficulty', 'questions_count', 'accuracy']
                        difficulty_performance['accuracy'] = difficulty_performance['accuracy'] * 100
                        
                        st.write("**Performance by Difficulty:**")
                        for _, row in difficulty_performance.iterrows():
                            st.metric(f"{row['difficulty']} Level", f"{row['accuracy']:.1f}%", f"{row['questions_count']} questions")
                
                with col2:
                    st.markdown("#### ⚡ Real-time Quiz Insights")
                    
                    # Current session stats
                    current_session = quiz_df[quiz_df['timestamp'].dt.date == datetime.now().date()]
                    session_accuracy = current_session['is_correct'].mean() * 100 if len(current_session) > 0 else 0
                    
                    st.metric("Today's Accuracy", f"{session_accuracy:.1f}%")
                    st.metric("Questions Today", len(current_session))
                    
                    # Strengths and weaknesses
                    if len(quiz_df) > 2:
                        st.write("**📈 Strengths & Weaknesses:**")
                        
                        if 'topic' in quiz_df.columns:
                            topic_acc = quiz_df.groupby('topic')['is_correct'].mean() * 100
                            best_topic = topic_acc.idxmax() if len(topic_acc) > 0 else "N/A"
                            worst_topic = topic_acc.idxmin() if len(topic_acc) > 0 else "N/A"
                            
                            st.success(f"💪 Strongest: {best_topic}")
                            st.warning(f"📚 Needs Practice: {worst_topic}")
                    
                    # Recent streak
                    recent_5 = quiz_df.tail(5)
                    if len(recent_5) > 0:
                        streak = 0
                        for correct in reversed(recent_5['is_correct'].tolist()):
                            if correct:
                                streak += 1
                            else:
                                break
                        
                        st.metric("Current Streak", f"{streak} correct")
                    
                    # Live learning progress
                    st.write("**🎯 Learning Progress:**")
                    progress_bar_value = min(session_accuracy / 100, 1.0) if session_accuracy > 0 else 0
                    st.progress(progress_bar_value)
                    st.write(f"Target: 80% accuracy (Current: {session_accuracy:.1f}%)")# TUTORIAL PAGE
elif page == "📚 Tutorial":
    st.title("📚 Platform Tutorial")
    
    tutorial_sections = [
        "🚀 Getting Started",
        "📊 Understanding Dashboards", 
        "🔬 EDA Analysis Guide",
        "⚡ Real-time Features",
        "🎮 Interactive Games",
        "💡 Best Practices"
    ]
    
    selected_section = st.selectbox("Choose tutorial section:", tutorial_sections)
    
    if selected_section == "🚀 Getting Started":
        st.markdown("""
        ## Welcome to CrowdCraft Analytics!
        
        ### What is this platform?
        This is a comprehensive user engagement analytics platform that helps you:
        - 📊 Visualize user data and engagement patterns
        - 🔬 Perform exploratory data analysis (EDA)
        - ⚡ Monitor real-time user activity
        - 🎮 Learn through interactive games
        
        ### How to navigate:
        1. Use the sidebar to switch between features
        2. Each page has specific functionality
        3. Interactive elements respond to your inputs
        4. Data updates automatically where applicable
        
        ### Quick Start:
        1. Visit the **Dashboard** to see overview metrics
        2. Check **Real-time Analytics** for live data
        3. Explore **EDA Analysis** for deep insights
        4. Try **Interactive Games** to test your knowledge
        """)
    
    elif selected_section == "📊 Understanding Dashboards":
        st.markdown("""
        ## Dashboard Guide
        
        ### Key Metrics:
        - **Total Users**: Number of registered users
        - **Total Events**: All user interactions tracked
        - **Avg Events/User**: Engagement level indicator
        - **Active Users**: Users with recent activity
        
        ### Visualizations:
        - **Pie Charts**: Show proportions and distributions
        - **Bar Charts**: Compare quantities across categories  
        - **Line Charts**: Display trends over time
        - **Heatmaps**: Reveal patterns in 2D data
        
        ### Filters:
        - Use date ranges to focus analysis
        - Filter by event types for specific insights
        - Combine filters for deeper analysis
        """)
    
    elif selected_section == "🔬 EDA Analysis Guide":
        st.markdown("""
        ## EDA (Exploratory Data Analysis) Guide
        
        ### What is EDA?
        EDA is the process of analyzing datasets to summarize their main characteristics, often using statistical graphics and other data visualization methods.
        
        ### Key Components:
        1. **Dataset Overview**: Basic statistics and structure
        2. **Distribution Analysis**: How data is spread
        3. **Correlation Analysis**: Relationships between variables
        4. **Pattern Detection**: Hidden insights in data
        
        ### EDA Best Practices:
        - Start with basic statistics
        - Use visualizations to spot patterns
        - Look for outliers and anomalies
        - Test assumptions about your data
        - Document findings and insights
        """)
    
    elif selected_section == "⚡ Real-time Features":
        st.markdown("""
        ## Real-time Analytics Guide
        
        ### Live Metrics:
        - **Active Users**: Currently online users
        - **Events/min**: Activity rate
        - **Bounce Rate**: Users leaving quickly
        - **Avg Session**: Time spent on platform
        
        ### Live Event Feed:
        - Shows recent user activities
        - Updates automatically
        - Helps monitor user behavior
        
        ### Auto-refresh:
        - Enable for continuous monitoring
        - Useful for live operations
        - Can be toggled on/off
        """)
    
    elif selected_section == "🎮 Interactive Games":
        st.markdown("""
        ## Gaming Features Guide
        
        ### Available Games:
        1. **Data Explorer Quiz**: Test analytics knowledge
        2. **Chart Master**: Learn visualization best practices
        3. **Pattern Detective**: Find hidden data patterns
        
        ### Learning Benefits:
        - Hands-on experience with data concepts
        - Interactive learning approach
        - Immediate feedback on answers
        - Gamified skill development
        
        ### Tips for Success:
        - Take time to analyze the data
        - Think about what the visualization shows
        - Consider the context of the question
        - Learn from incorrect answers
        """)
    
    elif selected_section == "💡 Best Practices":
        st.markdown("""
        ## Analytics Best Practices
        
        ### Data Analysis:
        - Always validate your data quality first
        - Look for patterns and anomalies
        - Consider seasonal trends and cycles
        - Cross-validate findings with multiple methods
        
        ### Visualization:
        - Choose appropriate chart types
        - Keep designs clean and readable
        - Use colors meaningfully
        - Include proper labels and titles
        
        ### Reporting:
        - Focus on actionable insights
        - Provide context for your findings
        - Use clear, non-technical language
        - Support conclusions with data evidence
        
        ### Continuous Improvement:
        - Regularly review and update dashboards
        - Gather feedback from stakeholders
        - Stay updated with new analytics techniques
        - Test and iterate on your approaches
        """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")
st.sidebar.markdown("CrowdCraft Analytics Platform 2025")
