@echo off
REM CrowdCraft Analytics - GitHub Setup Script for Windows

echo 🚀 Setting up CrowdCraft Analytics for GitHub and Streamlit Deployment
echo ==================================================================

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
)

REM Add all files
echo 📁 Adding all files to Git...
git add .

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "🚀 Deploy CrowdCraft Analytics Platform - Features: Interactive dashboards, Real-time analytics, EDA analysis, Gamified learning, Mobile-responsive design, Production-ready Streamlit deployment"

echo.
echo ✅ Git setup complete!
echo.
echo 🌐 Next steps for Streamlit Cloud deployment:
echo 1. Create a GitHub repository at https://github.com/new
echo 2. Run: git remote add origin https://github.com/yourusername/your-repo-name.git
echo 3. Run: git branch -M main
echo 4. Run: git push -u origin main
echo 5. Visit https://share.streamlit.io/ to deploy!
echo.
echo 📊 Your app will be live at: https://your-app-name.streamlit.app
echo.
pause
