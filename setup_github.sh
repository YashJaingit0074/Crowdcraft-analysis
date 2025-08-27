#!/bin/bash

# CrowdCraft Analytics - GitHub Setup Script
echo "🚀 Setting up CrowdCraft Analytics for GitHub and Streamlit Deployment"
echo "=================================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Add all files
echo "📁 Adding all files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🚀 Deploy CrowdCraft Analytics Platform

Features:
- Interactive dashboards with real-time filtering
- Live analytics monitoring and event streaming  
- Comprehensive EDA with statistical insights
- Gamified learning through interactive quizzes
- Mobile-responsive design for all devices
- Production-ready Streamlit deployment

Tech stack: Python, Streamlit, Pandas, Plotly, NumPy
Ready for Streamlit Cloud deployment!"

echo ""
echo "✅ Git setup complete!"
echo ""
echo "🌐 Next steps for Streamlit Cloud deployment:"
echo "1. Create a GitHub repository at https://github.com/new"
echo "2. Run: git remote add origin https://github.com/yourusername/your-repo-name.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
echo "5. Visit https://share.streamlit.io/ to deploy!"
echo ""
echo "📊 Your app will be live at: https://your-app-name.streamlit.app"
echo ""
