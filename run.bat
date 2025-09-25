@echo off
echo Starting Question Papers Platform...
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Setting up environment...
set FLASK_APP=backend/app.py
set FLASK_ENV=development

echo.
echo Starting Flask application...
python backend/app.py

pause