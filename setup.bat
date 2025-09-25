@echo off
echo Question Papers Platform Setup
echo ================================
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Set up MySQL database 'question_papers'
echo 2. Update database credentials in backend/config.py
echo 3. Run 'python init_db.py' to initialize the database
echo 4. Run 'run.bat' to start the application
echo.
echo Default admin credentials:
echo Username: admin
echo Password: admin123
echo.
pause