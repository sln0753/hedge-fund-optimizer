#!/bin/bash

# Portfolio Optimizer - Web App Launcher
# Simple script to start the Streamlit web interface

echo "================================================================================"
echo "                   PORTFOLIO OPTIMIZER - WEB INTERFACE                          "
echo "================================================================================"
echo ""
echo "Starting web application..."
echo ""
echo "The app will open automatically in your browser at:"
echo "http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "================================================================================"

# Navigate to script directory
cd "$(dirname "$0")"

# Launch Streamlit
streamlit run web_app.py


