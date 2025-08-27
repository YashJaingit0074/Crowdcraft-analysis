from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/home", tags=["navigation"])

@router.get("/", response_class=HTMLResponse)
async def unified_homepage():
    """Unified homepage with navigation to all features"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 User Engagement Analytics Platform</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }

            .header {
                text-align: center;
                margin-bottom: 50px;
                padding: 40px 0;
            }

            .header h1 {
                font-size: 3.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .header p {
                font-size: 1.3em;
                opacity: 0.9;
                margin-bottom: 20px;
            }

            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 30px;
                margin-bottom: 50px;
            }

            .feature-card {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.2);
                transition: all 0.4s ease;
                text-align: center;
                position: relative;
                overflow: hidden;
            }

            .feature-card::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: rotate(-45deg);
                transition: all 0.6s ease;
                opacity: 0;
            }

            .feature-card:hover::before {
                opacity: 1;
                transform: rotate(-45deg) translate(50%, 50%);
            }

            .feature-card:hover {
                transform: translateY(-10px) scale(1.02);
                border-color: rgba(255, 255, 255, 0.4);
                background: rgba(255, 255, 255, 0.15);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            }

            .feature-icon {
                font-size: 3em;
                margin-bottom: 20px;
                display: block;
            }

            .feature-card h3 {
                font-size: 1.5em;
                margin-bottom: 15px;
                color: #fff;
            }

            .feature-card p {
                opacity: 0.9;
                line-height: 1.6;
                margin-bottom: 25px;
            }

            .feature-btn {
                background: linear-gradient(135deg, #ff6b6b, #feca57);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .feature-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
                background: linear-gradient(135deg, #ff5252, #ff9800);
            }

            .feature-btn.primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
            }

            .feature-btn.primary:hover {
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                background: linear-gradient(135deg, #5a6fd8, #6a4190);
            }

            .feature-btn.success {
                background: linear-gradient(135deg, #56ab2f, #a8e6cf);
            }

            .feature-btn.success:hover {
                box-shadow: 0 8px 25px rgba(86, 171, 47, 0.4);
                background: linear-gradient(135deg, #4a9429, #96d4b8);
            }

            .feature-btn.warning {
                background: linear-gradient(135deg, #f093fb, #f5576c);
            }

            .feature-btn.warning:hover {
                box-shadow: 0 8px 25px rgba(240, 147, 251, 0.4);
                background: linear-gradient(135deg, #e081e8, #e34c5c);
            }

            .footer {
                text-align: center;
                padding: 30px 0;
                opacity: 0.8;
            }

            .quick-nav {
                position: fixed;
                bottom: 30px;
                right: 30px;
                background: rgba(0, 0, 0, 0.8);
                border-radius: 15px;
                padding: 20px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .quick-nav h4 {
                margin-bottom: 15px;
                color: #00ff88;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .quick-nav a {
                display: block;
                color: white;
                text-decoration: none;
                padding: 8px 15px;
                border-radius: 8px;
                margin: 5px 0;
                font-size: 0.9em;
                transition: all 0.3s ease;
            }

            .quick-nav a:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #00ff88;
                transform: translateX(5px);
            }

            .stats-banner {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 40px;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
            }

            .stat-item {
                text-align: center;
            }

            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #00ff88;
                display: block;
            }

            .stat-label {
                opacity: 0.8;
                font-size: 0.9em;
                margin-top: 5px;
            }

            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2.5em;
                }
                
                .features-grid {
                    grid-template-columns: 1fr;
                }
                
                .quick-nav {
                    position: static;
                    margin-top: 30px;
                }
            }

            /* Loading animation */
            .loading {
                display: none;
                text-align: center;
                padding: 50px;
            }

            .spinner {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top: 4px solid #00ff88;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 User Engagement Analytics Platform</h1>
                <p>Complete Interactive Analytics Suite with EDA, Real-time Monitoring & Gamification</p>
                
                <div class="stats-banner">
                    <div class="stats-grid">
                        <div class="stat-item">
                            <span class="stat-number">7+</span>
                            <span class="stat-label">Interactive Features</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">Real-time</span>
                            <span class="stat-label">Data Updates</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">EDA</span>
                            <span class="stat-label">Analysis Tools</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">Games</span>
                            <span class="stat-label">Learning Tools</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="features-grid">
                <!-- Interactive Dashboard -->
                <div class="feature-card">
                    <span class="feature-icon">📊</span>
                    <h3>Interactive Dashboard</h3>
                    <p>Comprehensive analytics dashboard with real-time charts, metrics, and interactive controls. View engagement patterns and trends with beautiful visualizations.</p>
                    <a href="/dashboard/" class="feature-btn primary" target="_blank">Launch Dashboard</a>
                </div>

                <!-- Live Real-time Analytics -->
                <div class="feature-card">
                    <span class="feature-icon">🔴</span>
                    <h3>Live Real-time Analytics</h3>
                    <p>Real-time monitoring dashboard with WebSocket connections, live activity feeds, and instant updates every 2 seconds.</p>
                    <a href="/realtime/live-dashboard" class="feature-btn warning" target="_blank">Go Live</a>
                </div>

                <!-- EDA Analysis -->
                <div class="feature-card">
                    <span class="feature-icon">🔍</span>
                    <h3>EDA Analysis Suite</h3>
                    <p>Complete Exploratory Data Analysis with user engagement patterns, temporal analysis, and optimization strategies identification.</p>
                    <a href="/docs#/eda-analysis" class="feature-btn success" target="_blank">Explore EDA</a>
                </div>

                <!-- Analytics Quiz Game -->
                <div class="feature-card">
                    <span class="feature-icon">🎮</span>
                    <h3>Analytics Quiz Challenge</h3>
                    <p>Interactive quiz game to test your analytics knowledge with 10 challenging questions, scoring system, and performance rankings.</p>
                    <a href="/games/analytics-quiz" class="feature-btn" target="_blank">Start Quiz</a>
                </div>

                <!-- Data Explorer Game -->
                <div class="feature-card">
                    <span class="feature-icon">🧭</span>
                    <h3>Data Explorer Game</h3>
                    <p>Interactive data exploration tool with multiple datasets, chart types, AI insights, and trend analysis capabilities.</p>
                    <a href="/games/data-explorer" class="feature-btn success" target="_blank">Explore Data</a>
                </div>

                <!-- API Documentation -->
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <h3>API Documentation</h3>
                    <p>Complete FastAPI documentation with interactive testing capabilities for all endpoints including events logging and analytics.</p>
                    <a href="/docs" class="feature-btn primary" target="_blank">View APIs</a>
                </div>

                <!-- Interactive Tutorial -->
                <div class="feature-card">
                    <span class="feature-icon">📚</span>
                    <h3>Interactive Tutorial</h3>
                    <p>Step-by-step guided tutorial to master all platform features with hands-on exercises and best practices.</p>
                    <a href="/tutorial/" class="feature-btn success" target="_blank">Start Tutorial</a>
                </div>
            </div>

            <div class="footer">
                <p>🚀 Built with FastAPI, SQLAlchemy, Plotly.js & WebSockets</p>
                <p>Complete analytics platform with interactive features and real-time capabilities</p>
            </div>
        </div>

        <!-- Quick Navigation -->
        <div class="quick-nav">
            <h4>🚀 Quick Access</h4>
            <a href="/dashboard/" target="_blank">📊 Dashboard</a>
            <a href="/realtime/live-dashboard" target="_blank">🔴 Live View</a>
            <a href="/games/analytics-quiz" target="_blank">🎮 Quiz</a>
            <a href="/games/data-explorer" target="_blank">🧭 Explorer</a>
            <a href="/tutorial/" target="_blank">📚 Tutorial</a>
            <a href="/docs" target="_blank">⚡ APIs</a>
        </div>

        <script>
            // Add some interactive effects
            document.addEventListener('DOMContentLoaded', function() {
                // Add click effects to buttons
                const buttons = document.querySelectorAll('.feature-btn');
                buttons.forEach(button => {
                    button.addEventListener('click', function(e) {
                        // Create ripple effect
                        const ripple = document.createElement('div');
                        ripple.style.position = 'absolute';
                        ripple.style.borderRadius = '50%';
                        ripple.style.background = 'rgba(255,255,255,0.6)';
                        ripple.style.transform = 'scale(0)';
                        ripple.style.animation = 'ripple 0.6s linear';
                        ripple.style.left = e.offsetX + 'px';
                        ripple.style.top = e.offsetY + 'px';
                        
                        this.style.position = 'relative';
                        this.appendChild(ripple);
                        
                        setTimeout(() => {
                            ripple.remove();
                        }, 600);
                    });
                });

                // Auto-update stats (demo)
                setInterval(() => {
                    const statNumbers = document.querySelectorAll('.stat-number');
                    // Add some dynamic effects if needed
                }, 5000);
            });

            // CSS for ripple effect
            const style = document.createElement('style');
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
