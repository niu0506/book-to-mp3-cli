@echo off
REM Book to MP3 Web Interface Startup Script for Windows

echo ========================================
echo   Book to MP3 Web Interface
echo ========================================
echo.
echo Starting web server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python -m src.web_server %*