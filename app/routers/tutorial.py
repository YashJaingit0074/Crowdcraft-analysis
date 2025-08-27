from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/tutorial", tags=["interactive-tutorial"])

@router.get("/", response_class=HTMLResponse)
async def interactive_tutorial():
    """Interactive step-by-step tutorial"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📚 Interactive Tutorial - Platform Guide</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                color: white;
                min-height: 100vh;
            }

            .tutorial-container {
                max-width: 900px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .tutorial-header {
                text-align: center;
                margin-bottom: 40px;
            }

            .tutorial-header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }

            .step {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 20px;
                border-left: 5px solid #00ff88;
                display: none;
            }

            .step.active {
                display: block;
                animation: slideIn 0.5s ease-in-out;
            }

            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }

            .step h3 {
                color: #00ff88;
                margin-bottom: 15px;
                font-size: 1.3em;
            }

            .step-content {
                line-height: 1.6;
            }

            .demo-area {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                padding: 20px;
                margin: 15px 0;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .btn {
                background: linear-gradient(135deg, #ff6b6b, #feca57);
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 25px;
                cursor: pointer;
                font-weight: bold;
                margin: 8px;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }

            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }

            .btn-primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
            }

            .btn-success {
                background: linear-gradient(135deg, #56ab2f, #a8e6cf);
            }

            .navigation {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 30px;
            }

            .step-counter {
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: bold;
            }

            .feature-card {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .code-block {
                background: rgba(0, 0, 0, 0.5);
                color: #00ff88;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                margin: 10px 0;
                border: 1px solid rgba(0, 255, 136, 0.3);
            }

            .highlight {
                background: linear-gradient(135deg, rgba(255, 107, 107, 0.3), rgba(254, 202, 87, 0.3));
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                border-left: 4px solid #ff6b6b;
            }

            .checklist {
                list-style: none;
                padding: 0;
            }

            .checklist li {
                padding: 8px 0;
                position: relative;
                padding-left: 30px;
            }

            .checklist li:before {
                content: '✅';
                position: absolute;
                left: 0;
            }
        </style>
    </head>
    <body>
        <div class="tutorial-container">
            <div class="tutorial-header">
                <h1>📚 Interactive Platform Tutorial</h1>
                <p>Step-by-step guide to master the User Engagement Analytics Platform</p>
            </div>

            <!-- Step 1: Welcome -->
            <div class="step active" id="step1">
                <h3>🚀 Step 1: Welcome to the Platform</h3>
                <div class="step-content">
                    <p>Welcome to the <strong>User Engagement Analytics Platform</strong>! Yeh complete suite hai analytics ke liye.</p>
                    
                    <div class="highlight">
                        <strong>🎯 What you'll learn:</strong>
                        <ul>
                            <li>Platform navigation</li>
                            <li>Each feature ka proper usage</li>
                            <li>API integration</li>
                            <li>Best practices</li>
                        </ul>
                    </div>

                    <div class="demo-area">
                        <h4>🌐 Platform Features:</h4>
                        <div class="feature-card">📊 Interactive Dashboard - Real-time analytics</div>
                        <div class="feature-card">🔴 Live Monitoring - WebSocket updates</div>
                        <div class="feature-card">🔍 EDA Analysis - Data exploration</div>
                        <div class="feature-card">🎮 Quiz Game - Learning tool</div>
                        <div class="feature-card">🧭 Data Explorer - Interactive exploration</div>
                        <div class="feature-card">⚡ REST APIs - Backend integration</div>
                    </div>

                    <p><strong>Ready to start?</strong> Click "Next Step" to begin the journey!</p>
                </div>
            </div>

            <!-- Step 2: Homepage Navigation -->
            <div class="step" id="step2">
                <h3>🏠 Step 2: Homepage Navigation</h3>
                <div class="step-content">
                    <p>Platform ka main entry point hai <strong>Homepage</strong>. Yahan se sab features accessible hain.</p>

                    <div class="demo-area">
                        <h4>🎯 Try This Now:</h4>
                        <ol>
                            <li>Open new tab: <a href="/home/" target="_blank" class="btn btn-primary">Open Homepage</a></li>
                            <li>Explore feature cards</li>
                            <li>Check right side quick navigation</li>
                            <li>Hover over cards for effects</li>
                        </ol>
                    </div>

                    <div class="code-block">
                        URL: http://localhost:8000/home/
                        Features: 6 interactive cards with direct access
                    </div>

                    <div class="highlight">
                        <strong>💡 Pro Tip:</strong> Use quick navigation menu on right side for instant access to any feature!
                    </div>
                </div>
            </div>

            <!-- Step 3: Interactive Dashboard -->
            <div class="step" id="step3">
                <h3>📊 Step 3: Interactive Dashboard</h3>
                <div class="step-content">
                    <p>Dashboard main comprehensive analytics view milta hai with real-time data.</p>

                    <div class="demo-area">
                        <h4>🎯 Hands-on Exercise:</h4>
                        <ol>
                            <li>Open dashboard: <a href="/dashboard/" target="_blank" class="btn btn-success">Launch Dashboard</a></li>
                            <li>Click "📊 Full EDA Analysis"</li>
                            <li>Wait for metrics cards to load</li>
                            <li>Interact with charts (hover/click)</li>
                            <li>Try other control buttons</li>
                        </ol>
                    </div>

                    <ul class="checklist">
                        <li>Metrics cards show live data</li>
                        <li>Charts are interactive with Plotly</li>
                        <li>Control buttons trigger different analyses</li>
                        <li>Auto-refresh functionality available</li>
                    </ul>

                    <div class="highlight">
                        <strong>🔥 Key Features:</strong> Real-time metrics, interactive charts, EDA integration, beautiful UI
                    </div>
                </div>
            </div>

            <!-- Step 4: Live Real-time Analytics -->
            <div class="step" id="step4">
                <h3>🔴 Step 4: Live Real-time Analytics</h3>
                <div class="step-content">
                    <p>Real-time dashboard WebSocket ke through live data updates show karta hai.</p>

                    <div class="demo-area">
                        <h4>🎯 Live Demo:</h4>
                        <ol>
                            <li>Open live dashboard: <a href="/realtime/live-dashboard" target="_blank" class="btn btn-warning">Go Live</a></li>
                            <li>Check connection status (top-right)</li>
                            <li>Watch metrics update every 2 seconds</li>
                            <li>Monitor activity feed (right side)</li>
                            <li>Observe live charts animation</li>
                        </ol>
                    </div>

                    <div class="code-block">
                        WebSocket: ws://localhost:8000/realtime/ws
                        Updates: Every 2 seconds
                        Features: Live metrics, activity feed, real-time charts
                    </div>

                    <ul class="checklist">
                        <li>🟢 Connection indicator shows status</li>
                        <li>📊 Metrics auto-update with animations</li>
                        <li>🚀 Activity feed shows live events</li>
                        <li>📈 Charts update in real-time</li>
                    </ul>
                </div>
            </div>

            <!-- Step 5: EDA Analysis -->
            <div class="step" id="step5">
                <h3>🔍 Step 5: EDA Analysis Suite</h3>
                <div class="step-content">
                    <p>EDA (Exploratory Data Analysis) complete data insights provide karta hai.</p>

                    <div class="demo-area">
                        <h4>🎯 API Testing:</h4>
                        <ol>
                            <li>Open API docs: <a href="/docs" target="_blank" class="btn btn-primary">View APIs</a></li>
                            <li>Find "eda-analysis" section</li>
                            <li>Try "GET /eda/engagement-analysis"</li>
                            <li>Click "Try it out" → "Execute"</li>
                            <li>Analyze the detailed results</li>
                        </ol>
                    </div>

                    <div class="highlight">
                        <strong>🔍 EDA Insights Include:</strong>
                        <ul>
                            <li>User engagement patterns</li>
                            <li>Top performer analysis</li>
                            <li>Temporal trends (peak hours/days)</li>
                            <li>Optimization recommendations</li>
                        </ul>
                    </div>

                    <div class="code-block">
                        GET /eda/engagement-analysis - Complete analysis
                        GET /eda/user-strengths - Top performers
                        GET /eda/optimization-strategies - Recommendations
                    </div>
                </div>
            </div>

            <!-- Step 6: Quiz Game -->
            <div class="step" id="step6">
                <h3>🎮 Step 6: Analytics Quiz Challenge</h3>
                <div class="step-content">
                    <p>Interactive quiz game analytics knowledge test करने के लिए, API-powered hai.</p>

                    <div class="demo-area">
                        <h4>🎯 Quiz Challenge:</h4>
                        <ol>
                            <li>Start quiz: <a href="/games/analytics-quiz" target="_blank" class="btn btn-success">Start Quiz</a></li>
                            <li>Choose difficulty: Easy/Medium/Hard</li>
                            <li>Answer questions with explanations</li>
                            <li>Submit quiz for detailed results</li>
                            <li>Check "Quiz Stats" for insights</li>
                        </ol>
                    </div>

                    <ul class="checklist">
                        <li>15+ questions in database</li>
                        <li>Multiple difficulty levels</li>
                        <li>Category-wise questions</li>
                        <li>Detailed explanations</li>
                        <li>Grade system (A+, A, B+, etc.)</li>
                    </ul>

                    <div class="code-block">
                        API: GET /quiz/questions?difficulty=easy
                        Submit: POST /quiz/submit
                        Stats: GET /quiz/stats
                    </div>
                </div>
            </div>

            <!-- Step 7: Data Explorer -->
            <div class="step" id="step7">
                <h3>🧭 Step 7: Data Explorer Game</h3>
                <div class="step-content">
                    <p>Interactive data exploration tool different datasets और chart types ke saath.</p>

                    <div class="demo-area">
                        <h4>🎯 Exploration Exercise:</h4>
                        <ol>
                            <li>Open explorer: <a href="/games/data-explorer" target="_blank" class="btn btn-warning">Explore Data</a></li>
                            <li>Load "Sales Data"</li>
                            <li>Try different chart types</li>
                            <li>Run "Trend Analysis"</li>
                            <li>Generate random data</li>
                            <li>Get "AI Insights"</li>
                        </ol>
                    </div>

                    <div class="highlight">
                        <strong>🔧 Available Tools:</strong>
                        <ul>
                            <li>Multiple datasets (Sales, Users, Traffic)</li>
                            <li>Chart types (Bar, Line, Pie)</li>
                            <li>Analysis tools (Trend, Correlation, Outliers)</li>
                            <li>AI-powered insights</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Step 8: API Integration -->
            <div class="step" id="step8">
                <h3>⚡ Step 8: API Integration</h3>
                <div class="step-content">
                    <p>Platform ke sare APIs ko integrate karna for custom applications.</p>

                    <div class="demo-area">
                        <h4>🎯 API Practice:</h4>
                        <div class="code-block">
# Log user event
curl -X POST "http://localhost:8000/events/" \\
  -H "Content-Type: application/json" \\
  -d '{"user_id": 1, "session_id": 1, "event_type": "click"}'

# Get analytics
curl -X GET "http://localhost:8000/analytics/event_counts"

# Quiz questions
curl -X GET "http://localhost:8000/quiz/questions?limit=5"
                        </div>
                    </div>

                    <ul class="checklist">
                        <li>Complete FastAPI documentation</li>
                        <li>Interactive testing interface</li>
                        <li>Request/Response examples</li>
                        <li>Error handling guidelines</li>
                    </ul>

                    <div class="highlight">
                        <strong>🚀 Best Practice:</strong> Always test APIs in /docs before integrating in your applications!
                    </div>
                </div>
            </div>

            <!-- Step 9: Best Practices -->
            <div class="step" id="step9">
                <h3>🎯 Step 9: Best Practices & Tips</h3>
                <div class="step-content">
                    <p>Platform ko effectively use करने के लिए important tips और best practices.</p>

                    <div class="demo-area">
                        <h4>💡 Pro Tips:</h4>
                        <ul class="checklist">
                            <li>Homepage को main navigation hub के रूप में use करें</li>
                            <li>Features को new tabs में open करें easy switching के लिए</li>
                            <li>Dashboard में "Full EDA Analysis" से start करें</li>
                            <li>Quiz में Easy mode से begin करें</li>
                            <li>API docs में "Try it out" feature use करें</li>
                            <li>Live dashboard connection status check करें</li>
                        </ul>
                    </div>

                    <div class="highlight">
                        <strong>🔧 Troubleshooting:</strong>
                        <ul>
                            <li>Page not loading → Refresh browser</li>
                            <li>API errors → Check /docs for correct format</li>
                            <li>Charts not showing → Wait for data loading</li>
                            <li>WebSocket issues → Refresh live dashboard</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Step 10: Conclusion -->
            <div class="step" id="step10">
                <h3>🎉 Step 10: Congratulations!</h3>
                <div class="step-content">
                    <p><strong>Congratulations!</strong> Tumne successfully complete platform ka tour kar liya hai! 🚀</p>

                    <div class="demo-area">
                        <h4>🎯 What You've Learned:</h4>
                        <ul class="checklist">
                            <li>Complete platform navigation</li>
                            <li>Interactive dashboard usage</li>
                            <li>Real-time monitoring</li>
                            <li>EDA analysis techniques</li>
                            <li>Quiz game participation</li>
                            <li>Data exploration tools</li>
                            <li>API integration methods</li>
                        </ul>
                    </div>

                    <div class="highlight">
                        <strong>🚀 Next Steps:</strong>
                        <ul>
                            <li>Practice with different datasets</li>
                            <li>Create custom API integrations</li>
                            <li>Explore advanced EDA features</li>
                            <li>Share insights with team</li>
                        </ul>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/home/" class="btn btn-success">🏠 Back to Homepage</a>
                        <button class="btn btn-primary" onclick="restartTutorial()">🔄 Restart Tutorial</button>
                    </div>
                </div>
            </div>

            <!-- Navigation -->
            <div class="navigation">
                <button class="btn" onclick="previousStep()" id="prevBtn" disabled>← Previous</button>
                <div class="step-counter">
                    Step <span id="currentStep">1</span> of 10
                </div>
                <button class="btn btn-primary" onclick="nextStep()" id="nextBtn">Next →</button>
            </div>
        </div>

        <script>
            let currentStepNum = 1;
            const totalSteps = 10;

            function showStep(stepNum) {
                // Hide all steps
                document.querySelectorAll('.step').forEach(step => {
                    step.classList.remove('active');
                });

                // Show current step
                document.getElementById(`step${stepNum}`).classList.add('active');

                // Update counter
                document.getElementById('currentStep').textContent = stepNum;

                // Update navigation buttons
                document.getElementById('prevBtn').disabled = stepNum === 1;
                document.getElementById('nextBtn').disabled = stepNum === totalSteps;
                
                if (stepNum === totalSteps) {
                    document.getElementById('nextBtn').textContent = 'Tutorial Complete!';
                } else {
                    document.getElementById('nextBtn').textContent = 'Next →';
                }
            }

            function nextStep() {
                if (currentStepNum < totalSteps) {
                    currentStepNum++;
                    showStep(currentStepNum);
                }
            }

            function previousStep() {
                if (currentStepNum > 1) {
                    currentStepNum--;
                    showStep(currentStepNum);
                }
            }

            function restartTutorial() {
                currentStepNum = 1;
                showStep(currentStepNum);
            }

            // Keyboard navigation
            document.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowRight') nextStep();
                if (e.key === 'ArrowLeft') previousStep();
            });

            // Initialize
            showStep(1);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
