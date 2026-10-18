@echo off
title AI Vision - ANN & Computer Vision
echo ========================================================
echo   Starting AI Vision Web Application...
echo   Artificial Neural Network & Computer Vision Project
echo ========================================================
cd /d "%~dp0"
.\.venv\Scripts\streamlit.exe run app.py
pause
