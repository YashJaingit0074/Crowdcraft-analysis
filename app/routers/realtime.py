from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import asyncio
from datetime import datetime
import random

router = APIRouter(prefix="/realtime", tags=["real-time"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@router.get("/live-dashboard", response_class=HTMLResponse)
async def live_dashboard():
    """Real-time live dashboard with WebSocket updates"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔴 LIVE - Real-time Analytics Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(45deg, #1e3c72, #2a5298);
                color: white;
                overflow-x: hidden;
            }
            .live-header {
                background: linear-gradient(135deg, #ff416c, #ff4b2b);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }
            .live-indicator {
                display: inline-flex;
                align-items: center;
                gap: 10px;
                background: rgba(255,255,255,0.2);
                padding: 10px 20px;
                border-radius: 25px;
                margin-top: 10px;
            }
            .pulse {
                width: 12px;
                height: 12px;
                background: #00ff00;
                border-radius: 50%;
                animation: pulse 1s infinite;
            }
            @keyframes pulse {
                0% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.2); opacity: 0.7; }
                100% { transform: scale(1); opacity: 1; }
            }
            .metrics-live {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                padding: 30px;
                max-width: 1400px;
                margin: 0 auto;
            }
            .metric-live {
                background: rgba(255,255,255,0.1);
                border: 2px solid rgba(255,255,255,0.2);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            .metric-live:hover {
                background: rgba(255,255,255,0.2);
                transform: translateY(-5px);
            }
            .metric-number {
                font-size: 3em;
                font-weight: bold;
                color: #00ff88;
                text-shadow: 0 0 20px rgba(0,255,136,0.5);
            }
            .metric-label {
                margin-top: 10px;
                opacity: 0.9;
                font-size: 1.1em;
            }
            .charts-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                padding: 30px;
                max-width: 1400px;
                margin: 0 auto;
            }
            .chart-live {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .activity-feed {
                position: fixed;
                top: 50%;
                right: 20px;
                transform: translateY(-50%);
                width: 300px;
                max-height: 60vh;
                background: rgba(0,0,0,0.8);
                border-radius: 15px;
                padding: 20px;
                overflow-y: auto;
                backdrop-filter: blur(10px);
            }
            .activity-item {
                padding: 10px;
                margin: 5px 0;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                font-size: 0.9em;
                border-left: 4px solid #00ff88;
            }
            .connection-status {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
                z-index: 1000;
            }
            .connected {
                background: #28a745;
                color: white;
            }
            .disconnected {
                background: #dc3545;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="connection-status disconnected" id="connectionStatus">
            🔴 Connecting...
        </div>

        <div class="live-header">
            <h1>🔴 LIVE ANALYTICS DASHBOARD</h1>
            <div class="live-indicator">
                <div class="pulse"></div>
                <span>Real-time Data Stream Active</span>
            </div>
        </div>

        <div class="metrics-live">
            <div class="metric-live">
                <div class="metric-number" id="liveUsers">0</div>
                <div class="metric-label">Active Users</div>
            </div>
            <div class="metric-live">
                <div class="metric-number" id="liveEvents">0</div>
                <div class="metric-label">Total Events</div>
            </div>
            <div class="metric-live">
                <div class="metric-number" id="liveEventsPerMin">0</div>
                <div class="metric-label">Events/Minute</div>
            </div>
            <div class="metric-live">
                <div class="metric-number" id="liveSessions">0</div>
                <div class="metric-label">Active Sessions</div>
            </div>
        </div>

        <div class="charts-container">
            <div class="chart-live">
                <div id="liveEventChart"></div>
            </div>
            <div class="chart-live">
                <div id="liveUserChart"></div>
            </div>
        </div>

        <div class="activity-feed">
            <h3>🚀 Live Activity Feed</h3>
            <div id="activityFeed"></div>
        </div>

        <script>
            const ws = new WebSocket(`ws://localhost:8000/realtime/ws`);
            let eventData = [];
            let userActivity = {};
            
            ws.onopen = function(event) {
                document.getElementById('connectionStatus').textContent = '🟢 Connected Live';
                document.getElementById('connectionStatus').className = 'connection-status connected';
            };
            
            ws.onclose = function(event) {
                document.getElementById('connectionStatus').textContent = '🔴 Disconnected';
                document.getElementById('connectionStatus').className = 'connection-status disconnected';
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateDashboard(data);
                addActivityFeed(data);
            };
            
            function updateDashboard(data) {
                // Update live metrics
                document.getElementById('liveUsers').textContent = data.active_users || 0;
                document.getElementById('liveEvents').textContent = data.total_events || 0;
                document.getElementById('liveEventsPerMin').textContent = data.events_per_minute || 0;
                document.getElementById('liveSessions').textContent = data.active_sessions || 0;
                
                // Update charts
                updateCharts(data);
            }
            
            function updateCharts(data) {
                // Live event chart
                if (data.event_timeline) {
                    const trace = [{
                        x: data.event_timeline.timestamps,
                        y: data.event_timeline.counts,
                        type: 'scatter',
                        mode: 'lines+markers',
                        line: { color: '#00ff88', width: 3 },
                        marker: { color: '#00ff88', size: 8 }
                    }];
                    
                    Plotly.newPlot('liveEventChart', trace, {
                        title: '📈 Real-time Event Stream',
                        paper_bgcolor: 'transparent',
                        plot_bgcolor: 'transparent',
                        font: { color: 'white' },
                        xaxis: { color: 'white', gridcolor: 'rgba(255,255,255,0.2)' },
                        yaxis: { color: 'white', gridcolor: 'rgba(255,255,255,0.2)' }
                    });
                }
                
                // User activity heatmap
                if (data.user_activity) {
                    const users = Object.keys(data.user_activity);
                    const activities = Object.values(data.user_activity);
                    
                    const trace = [{
                        x: users,
                        y: activities,
                        type: 'bar',
                        marker: { color: activities, colorscale: 'Viridis' }
                    }];
                    
                    Plotly.newPlot('liveUserChart', trace, {
                        title: '👥 Live User Activity',
                        paper_bgcolor: 'transparent',
                        plot_bgcolor: 'transparent',
                        font: { color: 'white' },
                        xaxis: { color: 'white', gridcolor: 'rgba(255,255,255,0.2)' },
                        yaxis: { color: 'white', gridcolor: 'rgba(255,255,255,0.2)' }
                    });
                }
            }
            
            function addActivityFeed(data) {
                const feed = document.getElementById('activityFeed');
                const now = new Date().toLocaleTimeString();
                
                const item = document.createElement('div');
                item.className = 'activity-item';
                item.innerHTML = `
                    <strong>${now}</strong><br>
                    ${data.activity_message || 'System update received'}
                `;
                
                feed.insertBefore(item, feed.firstChild);
                
                // Keep only last 20 items
                while (feed.children.length > 20) {
                    feed.removeChild(feed.lastChild);
                }
            }
            
            // Simulate some activity for demo
            setTimeout(() => {
                setInterval(() => {
                    const mockData = {
                        active_users: Math.floor(Math.random() * 100) + 50,
                        total_events: Math.floor(Math.random() * 1000) + 500,
                        events_per_minute: Math.floor(Math.random() * 50) + 10,
                        active_sessions: Math.floor(Math.random() * 30) + 20,
                        activity_message: `New ${['login', 'purchase', 'click', 'view'][Math.floor(Math.random() * 4)]} event detected`,
                        event_timeline: {
                            timestamps: Array.from({length: 20}, (_, i) => new Date(Date.now() - i * 60000).toLocaleTimeString()),
                            counts: Array.from({length: 20}, () => Math.floor(Math.random() * 30) + 5)
                        },
                        user_activity: {
                            'User1': Math.floor(Math.random() * 50),
                            'User2': Math.floor(Math.random() * 50),
                            'User3': Math.floor(Math.random() * 50),
                            'User4': Math.floor(Math.random() * 50),
                            'User5': Math.floor(Math.random() * 50)
                        }
                    };
                    
                    if (ws.readyState === WebSocket.OPEN) {
                        updateDashboard(mockData);
                        addActivityFeed(mockData);
                    }
                }, 2000);
            }, 1000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send live data every 2 seconds
            live_data = {
                "active_users": random.randint(20, 100),
                "total_events": random.randint(500, 2000),
                "events_per_minute": random.randint(5, 50),
                "active_sessions": random.randint(10, 40),
                "activity_message": f"User performed {random.choice(['login', 'click', 'purchase', 'search'])} action",
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send_text(json.dumps(live_data))
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
