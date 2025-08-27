from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import random
from datetime import datetime

router = APIRouter(prefix="/games", tags=["interactive-games"])

@router.get("/analytics-quiz", response_class=HTMLResponse)
async def analytics_quiz_game():
    """Interactive quiz game with API integration"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎮 Analytics Quiz Challenge - API Powered</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .quiz-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                padding: 40px;
                max-width: 700px;
                width: 90%;
                text-align: center;
            }
            .quiz-header {
                margin-bottom: 30px;
            }
            .quiz-header h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .api-badge {
                background: linear-gradient(135deg, #00ff88, #00cc6a);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                font-weight: bold;
                margin: 10px;
                display: inline-block;
            }
            .controls {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }
            .control-btn {
                background: linear-gradient(135def, #4ecdc4, #44a08d);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .control-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .score {
                background: linear-gradient(135deg, #56ab2f, #a8e6cf);
                color: white;
                padding: 15px;
                border-radius: 10px;
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 30px;
            }
            .question {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                text-align: left;
            }
            .question h3 {
                color: #333;
                margin-bottom: 20px;
                font-size: 1.3em;
            }
            .question-meta {
                display: flex;
                gap: 15px;
                margin-bottom: 15px;
                font-size: 0.9em;
            }
            .difficulty-badge {
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 0.8em;
            }
            .difficulty-easy { background: #28a745; color: white; }
            .difficulty-medium { background: #ffc107; color: black; }
            .difficulty-hard { background: #dc3545; color: white; }
            .category-badge {
                background: #17a2b8;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 0.8em;
            }
            .option {
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            .option:hover {
                border-color: #667eea;
                background: #f0f7ff;
            }
            .option.selected {
                border-color: #667eea;
                background: #667eea;
                color: white;
            }
            .option.correct {
                border-color: #28a745;
                background: #28a745;
                color: white;
            }
            .option.incorrect {
                border-color: #dc3545;
                background: #dc3545;
                color: white;
            }
            .explanation {
                background: #e8f5e8;
                border-left: 4px solid #28a745;
                padding: 15px;
                margin-top: 15px;
                border-radius: 0 8px 8px 0;
                font-style: italic;
            }
            .btn {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 10px;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .progress-bar {
                background: #e9ecef;
                border-radius: 10px;
                height: 10px;
                margin-bottom: 20px;
                overflow: hidden;
            }
            .progress {
                background: linear-gradient(135deg, #667eea, #764ba2);
                height: 100%;
                transition: width 0.3s ease;
            }
            .result {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 30px;
                margin-top: 20px;
            }
            .loading {
                text-align: center;
                padding: 50px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .api-info {
                background: rgba(102, 126, 234, 0.1);
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="quiz-container">
            <div class="quiz-header">
                <h1>🎮 Analytics Quiz Challenge</h1>
                <div class="api-badge">⚡ API Powered</div>
                <div class="api-info">
                    <strong>🚀 Dynamic Quiz:</strong> Questions loaded from FastAPI backend with real-time scoring and detailed explanations!
                </div>
                <div class="progress-bar">
                    <div class="progress" id="progressBar" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="controls">
                <button class="control-btn" onclick="loadQuiz('easy')">Easy Mode</button>
                <button class="control-btn" onclick="loadQuiz('medium')">Medium Mode</button>
                <button class="control-btn" onclick="loadQuiz('hard')">Hard Mode</button>
                <button class="control-btn" onclick="loadRandomQuiz()">Random Mix</button>
                <button class="control-btn" onclick="showQuizStats()">Quiz Stats</button>
            </div>
            
            <div class="score" id="scoreDisplay">
                Score: <span id="score">0</span> / <span id="total">0</span>
                <span id="percentage"></span>
            </div>
            
            <div id="quizContent">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading quiz from API...</p>
                </div>
            </div>
            
            <div>
                <button class="btn" id="nextBtn" onclick="nextQuestion()" disabled>Next Question</button>
                <button class="btn" onclick="submitQuiz()">Submit Quiz</button>
                <button class="btn" onclick="restartQuiz()">New Quiz</button>
            </div>
        </div>

        <script>
            let currentQuestions = [];
            let currentQuestionIndex = 0;
            let userAnswers = [];
            let selectedOption = -1;
            let quizActive = false;

            async function loadQuiz(difficulty = null) {
                try {
                    showLoading();
                    
                    let url = '/quiz/questions?limit=10';
                    if (difficulty) {
                        url += `&difficulty=${difficulty}`;
                    }
                    
                    const response = await fetch(url);
                    const questions = await response.json();
                    
                    if (questions.length === 0) {
                        throw new Error('No questions found');
                    }
                    
                    currentQuestions = questions;
                    currentQuestionIndex = 0;
                    userAnswers = [];
                    quizActive = true;
                    
                    document.getElementById('total').textContent = questions.length;
                    document.getElementById('score').textContent = '0';
                    document.getElementById('percentage').textContent = '';
                    
                    loadCurrentQuestion();
                    
                } catch (error) {
                    showError('Failed to load quiz: ' + error.message);
                }
            }

            async function loadRandomQuiz() {
                await loadQuiz(); // Load without difficulty filter
            }

            function loadCurrentQuestion() {
                if (currentQuestionIndex >= currentQuestions.length) {
                    finishQuiz();
                    return;
                }

                const question = currentQuestions[currentQuestionIndex];
                const content = document.getElementById('quizContent');
                
                const difficultyClass = `difficulty-${question.difficulty.toLowerCase()}`;
                
                content.innerHTML = `
                    <div class="question">
                        <div class="question-meta">
                            <span class="difficulty-badge ${difficultyClass}">${question.difficulty}</span>
                            <span class="category-badge">${question.category}</span>
                        </div>
                        <h3>Question ${currentQuestionIndex + 1}: ${question.question}</h3>
                        ${question.options.map((option, index) => `
                            <div class="option" onclick="selectOption(${index})">
                                ${String.fromCharCode(65 + index)}. ${option}
                            </div>
                        `).join('')}
                    </div>
                `;
                
                updateProgress();
                document.getElementById('nextBtn').disabled = true;
                selectedOption = -1;
            }

            function selectOption(index) {
                if (!quizActive) return;
                
                selectedOption = index;
                const options = document.querySelectorAll('.option');
                options.forEach((opt, i) => {
                    opt.classList.remove('selected');
                    if (i === index) {
                        opt.classList.add('selected');
                    }
                });
                document.getElementById('nextBtn').disabled = false;
            }

            function nextQuestion() {
                if (selectedOption === -1) return;

                const question = currentQuestions[currentQuestionIndex];
                
                // Store user answer
                userAnswers.push({
                    question_id: question.id,
                    selected_option: selectedOption
                });

                // Show correct answer
                const options = document.querySelectorAll('.option');
                options.forEach((opt, index) => {
                    opt.style.pointerEvents = 'none';
                    if (index === question.correct) {
                        opt.classList.add('correct');
                    } else if (index === selectedOption && index !== question.correct) {
                        opt.classList.add('incorrect');
                    }
                });

                // Show explanation
                const questionDiv = document.querySelector('.question');
                questionDiv.innerHTML += `
                    <div class="explanation">
                        <strong>💡 Explanation:</strong> ${question.explanation}
                    </div>
                `;

                // Update score if correct
                if (selectedOption === question.correct) {
                    const newScore = parseInt(document.getElementById('score').textContent) + 1;
                    document.getElementById('score').textContent = newScore;
                    
                    const percentage = Math.round((newScore / currentQuestions.length) * 100);
                    document.getElementById('percentage').textContent = `(${percentage}%)`;
                }

                setTimeout(() => {
                    currentQuestionIndex++;
                    if (currentQuestionIndex < currentQuestions.length) {
                        loadCurrentQuestion();
                    } else {
                        finishQuiz();
                    }
                }, 3000);
            }

            async function submitQuiz() {
                if (!quizActive || userAnswers.length === 0) {
                    alert('Please answer some questions first!');
                    return;
                }

                try {
                    showLoading();
                    
                    const response = await fetch('/quiz/submit', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(userAnswers)
                    });
                    
                    const result = await response.json();
                    showDetailedResults(result);
                    
                } catch (error) {
                    showError('Failed to submit quiz: ' + error.message);
                }
            }

            function finishQuiz() {
                quizActive = false;
                document.getElementById('nextBtn').style.display = 'none';
                submitQuiz();
            }

            function showDetailedResults(result) {
                const content = document.getElementById('quizContent');
                
                let resultHTML = `
                    <div class="result">
                        <h2>🎯 Quiz Results</h2>
                        <div style="font-size: 1.2em; margin: 20px 0;">
                            <strong>Grade: ${result.grade}</strong><br>
                            Score: ${result.correct_answers}/${result.total_questions} (${result.score_percentage}%)
                        </div>
                        <h3>📊 Detailed Breakdown:</h3>
                `;

                result.answers.forEach((answer, index) => {
                    const icon = answer.is_correct ? '✅' : '❌';
                    const statusClass = answer.is_correct ? 'correct' : 'incorrect';
                    
                    resultHTML += `
                        <div style="margin: 15px 0; padding: 15px; border-radius: 8px; background: ${answer.is_correct ? '#e8f5e8' : '#ffeaea'};">
                            <strong>${icon} Q${index + 1}:</strong> ${answer.question}<br>
                            <em>Category: ${answer.category} | Difficulty: ${answer.difficulty}</em><br>
                            <small><strong>Explanation:</strong> ${answer.explanation}</small>
                        </div>
                    `;
                });

                resultHTML += '</div>';
                content.innerHTML = resultHTML;
            }

            async function showQuizStats() {
                try {
                    const response = await fetch('/quiz/stats');
                    const stats = await response.json();
                    
                    let statsHTML = `
                        <div class="result">
                            <h3>📊 Quiz Statistics</h3>
                            <p><strong>Total Questions Available:</strong> ${stats.total_questions}</p>
                            <h4>By Category:</h4>
                            <ul>
                    `;
                    
                    Object.entries(stats.categories).forEach(([category, count]) => {
                        statsHTML += `<li>${category}: ${count} questions</li>`;
                    });
                    
                    statsHTML += `
                            </ul>
                            <h4>By Difficulty:</h4>
                            <ul>
                    `;
                    
                    Object.entries(stats.difficulties).forEach(([difficulty, count]) => {
                        statsHTML += `<li>${difficulty}: ${count} questions</li>`;
                    });
                    
                    statsHTML += `
                            </ul>
                        </div>
                    `;
                    
                    document.getElementById('quizContent').innerHTML = statsHTML;
                    
                } catch (error) {
                    showError('Failed to load stats: ' + error.message);
                }
            }

            function updateProgress() {
                if (currentQuestions.length === 0) return;
                const progress = ((currentQuestionIndex + 1) / currentQuestions.length) * 100;
                document.getElementById('progressBar').style.width = progress + '%';
            }

            function showLoading() {
                document.getElementById('quizContent').innerHTML = `
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Loading from API...</p>
                    </div>
                `;
            }

            function showError(message) {
                document.getElementById('quizContent').innerHTML = `
                    <div class="result">
                        <h3>❌ Error</h3>
                        <p>${message}</p>
                        <button class="btn" onclick="loadRandomQuiz()">Try Again</button>
                    </div>
                `;
            }

            function restartQuiz() {
                loadRandomQuiz();
                document.getElementById('nextBtn').style.display = 'inline-block';
            }

            // Auto-load quiz on page load
            window.onload = function() {
                loadRandomQuiz();
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/data-explorer", response_class=HTMLResponse)
async def interactive_data_explorer():
    """Interactive data exploration game"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔍 Data Explorer Game</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(45deg, #1e3c72, #2a5298);
                margin: 0;
                padding: 20px;
                color: white;
                min-height: 100vh;
            }
            .explorer-container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .controls {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .control-group {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            .control-group h3 {
                margin-top: 0;
                color: #00ff88;
            }
            .btn-game {
                background: linear-gradient(135deg, #ff6b6b, #feca57);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                cursor: pointer;
                font-weight: bold;
                margin: 5px;
                transition: all 0.3s ease;
            }
            .btn-game:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .chart-container {
                background: rgba(255,255,255,0.05);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .insight-box {
                background: rgba(0,255,136,0.2);
                border: 2px solid #00ff88;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }
            .insight-box h3 {
                color: #00ff88;
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <div class="explorer-container">
            <div class="header">
                <h1>🔍 Interactive Data Explorer</h1>
                <p>Explore different datasets and discover insights!</p>
            </div>

            <div class="controls">
                <div class="control-group">
                    <h3>📊 Dataset</h3>
                    <button class="btn-game" onclick="loadDataset('sales')">Sales Data</button>
                    <button class="btn-game" onclick="loadDataset('users')">User Behavior</button>
                    <button class="btn-game" onclick="loadDataset('traffic')">Website Traffic</button>
                </div>
                
                <div class="control-group">
                    <h3>📈 Chart Type</h3>
                    <button class="btn-game" onclick="changeChart('bar')">Bar Chart</button>
                    <button class="btn-game" onclick="changeChart('line')">Line Chart</button>
                    <button class="btn-game" onclick="changeChart('pie')">Pie Chart</button>
                </div>
                
                <div class="control-group">
                    <h3>🎯 Analysis</h3>
                    <button class="btn-game" onclick="runAnalysis('trend')">Trend Analysis</button>
                    <button class="btn-game" onclick="runAnalysis('correlation')">Correlations</button>
                    <button class="btn-game" onclick="runAnalysis('outliers')">Find Outliers</button>
                </div>
                
                <div class="control-group">
                    <h3>⚡ Actions</h3>
                    <button class="btn-game" onclick="generateRandomData()">Random Data</button>
                    <button class="btn-game" onclick="exploreInsights()">AI Insights</button>
                </div>
            </div>

            <div class="chart-container">
                <div id="explorerChart"></div>
            </div>

            <div class="insight-box" id="insightBox" style="display: none;">
                <h3>💡 Data Insights</h3>
                <div id="insightContent"></div>
            </div>
        </div>

        <script>
            let currentData = null;
            let currentChart = 'bar';

            const datasets = {
                sales: {
                    name: 'Sales Performance',
                    data: {
                        categories: ['Q1', 'Q2', 'Q3', 'Q4'],
                        values: [45000, 62000, 58000, 71000],
                        colors: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24']
                    },
                    insights: [
                        'Q4 shows 22% growth compared to Q1',
                        'Steady upward trend with minor Q3 dip',
                        'Average quarterly growth: 12%'
                    ]
                },
                users: {
                    name: 'User Engagement',
                    data: {
                        categories: ['Login', 'Click', 'Purchase', 'Share', 'Comment'],
                        values: [1200, 850, 320, 180, 95],
                        colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
                    },
                    insights: [
                        'Login events dominate at 47% of all interactions',
                        'Purchase conversion rate: 26.7%',
                        'Social engagement (share+comment) is low at 11%'
                    ]
                },
                traffic: {
                    name: 'Website Traffic Sources',
                    data: {
                        categories: ['Direct', 'Social Media', 'Search', 'Email', 'Referral'],
                        values: [35, 28, 22, 10, 5],
                        colors: ['#ff9a9e', '#fecfef', '#fecfef', '#fad0c4', '#ffd1ff']
                    },
                    insights: [
                        'Direct traffic is the primary source (35%)',
                        'Social media contributes 28% of traffic',
                        'Email marketing needs improvement (10%)'
                    ]
                }
            };

            function loadDataset(type) {
                currentData = datasets[type];
                updateChart();
                showInsights();
            }

            function changeChart(type) {
                currentChart = type;
                if (currentData) updateChart();
            }

            function updateChart() {
                if (!currentData) return;

                let trace;
                const data = currentData.data;

                switch (currentChart) {
                    case 'bar':
                        trace = [{
                            x: data.categories,
                            y: data.values,
                            type: 'bar',
                            marker: { color: data.colors }
                        }];
                        break;
                    
                    case 'line':
                        trace = [{
                            x: data.categories,
                            y: data.values,
                            type: 'scatter',
                            mode: 'lines+markers',
                            line: { color: '#00ff88', width: 4 },
                            marker: { color: data.colors, size: 10 }
                        }];
                        break;
                    
                    case 'pie':
                        trace = [{
                            labels: data.categories,
                            values: data.values,
                            type: 'pie',
                            marker: { colors: data.colors }
                        }];
                        break;
                }

                Plotly.newPlot('explorerChart', trace, {
                    title: `${currentData.name} - ${currentChart.toUpperCase()} Chart`,
                    paper_bgcolor: 'transparent',
                    plot_bgcolor: 'transparent',
                    font: { color: 'white', size: 14 }
                });
            }

            function runAnalysis(type) {
                if (!currentData) {
                    alert('Please load a dataset first!');
                    return;
                }

                let analysis = '';
                const values = currentData.data.values;
                
                switch (type) {
                    case 'trend':
                        const trend = values[values.length - 1] > values[0] ? 'Upward' : 'Downward';
                        analysis = `📈 Trend Analysis: ${trend} trend detected. Average value: ${(values.reduce((a,b) => a+b) / values.length).toFixed(0)}`;
                        break;
                    
                    case 'correlation':
                        analysis = '🔗 Correlation Analysis: Strong positive correlation found between categories and performance metrics.';
                        break;
                    
                    case 'outliers':
                        const max = Math.max(...values);
                        const maxIndex = values.indexOf(max);
                        analysis = `🎯 Outlier Detection: Highest value found in "${currentData.data.categories[maxIndex]}" at ${max}`;
                        break;
                }

                showInsights(analysis);
            }

            function generateRandomData() {
                const categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E'];
                const values = categories.map(() => Math.floor(Math.random() * 1000) + 100);
                const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#a8e6cf'];

                currentData = {
                    name: 'Random Dataset',
                    data: { categories, values, colors },
                    insights: [
                        'This is randomly generated data',
                        `Highest value: ${Math.max(...values)}`,
                        `Total sum: ${values.reduce((a,b) => a+b)}`
                    ]
                };

                updateChart();
                showInsights();
            }

            function exploreInsights() {
                if (!currentData) {
                    alert('Load a dataset first!');
                    return;
                }

                const aiInsights = [
                    '🤖 AI detected seasonal patterns in your data',
                    '📊 Recommended focus on top-performing categories',
                    '⚡ Suggested A/B testing for underperforming segments',
                    '🎯 Identified optimization opportunities',
                    '📈 Predicted 15% growth potential with current trends'
                ];

                const randomInsight = aiInsights[Math.floor(Math.random() * aiInsights.length)];
                showInsights(randomInsight);
            }

            function showInsights(customInsight = null) {
                if (!currentData) return;

                const box = document.getElementById('insightBox');
                const content = document.getElementById('insightContent');
                
                let insights = customInsight ? [customInsight] : currentData.insights;
                
                content.innerHTML = `
                    <ul>
                        ${insights.map(insight => `<li>${insight}</li>`).join('')}
                    </ul>
                `;
                
                box.style.display = 'block';
            }

            // Load default dataset
            loadDataset('sales');
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
