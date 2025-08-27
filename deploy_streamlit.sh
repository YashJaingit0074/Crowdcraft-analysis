#!/bin/bash

# CrowdCraft Analytics - Streamlit Deployment Script
# Run this script to deploy your analytics platform on Streamlit

echo "🚀 CrowdCraft Analytics - Streamlit Deployment"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source .venv/Scripts/activate

# Install Streamlit requirements
echo "📥 Installing Streamlit dependencies..."
pip install -r streamlit_requirements.txt

# Install additional requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "📥 Installing additional dependencies..."
    pip install pandas plotly numpy
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "🎯 To run your Streamlit app locally:"
echo "   streamlit run streamlit_app.py"
echo ""
echo "🌐 To deploy on Streamlit Cloud:"
echo "   1. Push code to GitHub"
echo "   2. Go to https://share.streamlit.io/"
echo "   3. Connect your GitHub repository"
echo "   4. Set main file as 'streamlit_app.py'"
echo ""
echo "🔧 App will be available at: http://localhost:8501"
echo ""
