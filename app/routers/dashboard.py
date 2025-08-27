from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.eda_analysis import EngagementEDA
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly

router = APIRouter(prefix="/dashboard", tags=["interactive-dashboard"])

load_dotenv()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_class=HTMLResponse)
async def interactive_dashboard():
    """Interactive dashboard with real-time charts"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 User Engagement Analytics Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #ff6b6b, #feca57);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .controls {
                padding: 20px;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            .btn-success {
                background: linear-gradient(135deg, #56ab2f, #a8e6cf);
                color: white;
            }
            .btn-warning {
                background: linear-gradient(135deg, #f093fb, #f5576c);
                color: white;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            .chart-container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                padding: 20px;
            }
            .metrics-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
                padding: 0 20px;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .metric-label {
                opacity: 0.9;
                font-size: 0.9em;
            }
            .loading {
                text-align: center;
                padding: 50px;
                font-size: 1.2em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 User Engagement Analytics Dashboard</h1>
                <p>Interactive Real-time Analytics & EDA Insights</p>
            </div>
            
            <div class="controls">
                <button class="btn btn-primary" onclick="loadEngagementAnalysis()">
                    📊 Full EDA Analysis
                </button>
                <button class="btn btn-success" onclick="loadUserStrengths()">
                    🌟 User Strengths
                </button>
                <button class="btn btn-warning" onclick="loadOptimizations()">
                    🎯 Optimization Tips
                </button>
                <button class="btn btn-primary" onclick="loadRealTimeData()">
                    🔄 Refresh Data
                </button>
            </div>

            <div class="metrics-container" id="metricsContainer">
                <!-- Metrics cards will be loaded here -->
            </div>

            <div class="dashboard-grid">
                <div class="chart-container">
                    <div id="eventChart">
                        <div class="loading">📊 Loading Event Distribution...</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div id="userChart">
                        <div class="loading">👥 Loading User Activity...</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div id="timeChart">
                        <div class="loading">⏰ Loading Time Patterns...</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div id="insightsChart">
                        <div class="loading">💡 Loading Insights...</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Auto-load dashboard on page load
            window.onload = function() {
                loadEngagementAnalysis();
            };

            function loadEngagementAnalysis() {
                showLoading();
                fetch('/eda/engagement-analysis')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            displayMetrics(data.insights.basic_metrics);
                            displayCharts(data.insights);
                        } else {
                            showError('Failed to load engagement analysis');
                        }
                    })
                    .catch(error => {
                        showError('Error: ' + error.message);
                    });
            }

            function loadUserStrengths() {
                fetch('/eda/user-strengths')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            displayUserStrengths(data);
                        }
                    });
            }

            function loadOptimizations() {
                fetch('/eda/optimization-strategies')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            displayOptimizations(data);
                        }
                    });
            }

            function displayMetrics(metrics) {
                const container = document.getElementById('metricsContainer');
                container.innerHTML = `
                    <div class="metric-card">
                        <div class="metric-value">${metrics.total_users}</div>
                        <div class="metric-label">Total Users</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${metrics.total_events}</div>
                        <div class="metric-label">Total Events</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${Object.keys(metrics.event_distribution).length}</div>
                        <div class="metric-label">Event Types</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${(metrics.total_events / metrics.total_users).toFixed(1)}</div>
                        <div class="metric-label">Avg Events/User</div>
                    </div>
                `;
            }

            function displayCharts(insights) {
                // Event distribution pie chart
                const eventData = insights.basic_metrics.event_distribution;
                const eventTrace = [{
                    values: Object.values(eventData),
                    labels: Object.keys(eventData),
                    type: 'pie',
                    marker: {
                        colors: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FFB6C1']
                    }
                }];
                
                Plotly.newPlot('eventChart', eventTrace, {
                    title: '📊 Event Type Distribution',
                    font: { family: 'Segoe UI' }
                });

                // Time patterns
                if (insights.temporal_patterns) {
                    const hourlyData = insights.temporal_patterns.hourly_distribution;
                    const hourlyTrace = [{
                        x: Object.keys(hourlyData),
                        y: Object.values(hourlyData),
                        type: 'bar',
                        marker: { color: '#667eea' }
                    }];
                    
                    Plotly.newPlot('timeChart', hourlyTrace, {
                        title: '⏰ Hourly Activity Patterns',
                        xaxis: { title: 'Hour of Day' },
                        yaxis: { title: 'Number of Events' }
                    });
                }
            }

            function displayUserStrengths(data) {
                const topUsers = data.top_performers;
                const userNames = Object.keys(topUsers).slice(0, 10);
                const userEvents = userNames.map(name => topUsers[name].total_events);
                
                const trace = [{
                    x: userNames,
                    y: userEvents,
                    type: 'bar',
                    marker: { color: '#56ab2f' }
                }];
                
                Plotly.newPlot('userChart', trace, {
                    title: '🌟 Top User Performance',
                    xaxis: { title: 'Users' },
                    yaxis: { title: 'Total Events' }
                });
            }

            function displayOptimizations(data) {
                const insights = data.optimization_opportunities;
                document.getElementById('insightsChart').innerHTML = `
                    <h3>🎯 Optimization Insights</h3>
                    <ul style="font-size: 16px; line-height: 1.8;">
                        <li><strong>Low Engagement Users:</strong> ${insights.low_engagement_count} users need attention</li>
                        <li><strong>Session Length:</strong> Current average is ${insights.avg_session_length.toFixed(1)} minutes</li>
                        <li><strong>Priority Actions:</strong></li>
                    </ul>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 15px;">
                        ${data.action_items.map(item => `<div style="margin: 8px 0;">• ${item}</div>`).join('')}
                    </div>
                `;
            }

            function showLoading() {
                document.querySelectorAll('.loading').forEach(el => {
                    el.style.display = 'block';
                });
            }

            function showError(message) {
                alert('Error: ' + message);
            }

            function loadRealTimeData() {
                loadEngagementAnalysis();
                setTimeout(() => {
                    loadUserStrengths();
                    loadOptimizations();
                }, 1000);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/live-metrics")
async def get_live_metrics():
    """Get live metrics for real-time updates"""
    try:
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/analytics')
        sync_db_url = db_url.replace('+asyncpg', '')
        
        eda = EngagementEDA(sync_db_url)
        eda.load_data()
        
        # Calculate live metrics
        total_events = len(eda.events_df)
        total_users = eda.events_df['user_id'].nunique()
        recent_events = len(eda.events_df[eda.events_df['timestamp'] > (eda.events_df['timestamp'].max() - pd.Timedelta(hours=24))])
        
        return {
            "total_events": total_events,
            "total_users": total_users,
            "recent_events_24h": recent_events,
            "avg_events_per_user": round(total_events / total_users, 2) if total_users > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
