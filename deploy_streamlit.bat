@echo off
REM CrowdCraft Analytics - Streamlit Deployment Script for Windows
REM Run this script to deploy your analytics platform on Streamlit

echo 🚀 CrowdCraft Analytics - Streamlit Deployment
echo ==============================================

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install Streamlit requirements
echo 📥 Installing Streamlit dependencies...
pip install streamlit==1.28.0 pandas==2.0.3 numpy==1.24.3 plotly==5.15.0

REM Install additional requirements if they exist
if exist "requirements.txt" (
    echo 📥 Installing additional dependencies...
    pip install pandas plotly numpy
)

echo.
echo ✅ Setup completed!
echo.
echo 🎯 To run your Streamlit app locally:
echo    streamlit run streamlit_app.py
echo.
echo 🌐 To deploy on Streamlit Cloud:
echo    1. Push code to GitHub
echo    2. Go to https://share.streamlit.io/
echo    3. Connect your GitHub repository  
echo    4. Set main file as 'streamlit_app.py'
echo.
echo 🔧 App will be available at: http://localhost:8501
echo.
pause
