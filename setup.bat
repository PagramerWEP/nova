@echo off
echo Setting up the Student Activities Management System...
echo ===========================================

:: Create and activate virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Install requirements
echo Installing requirements...
pip install -r backend\requirements.txt

:: Set up database
echo Setting up database...
cd backend
python manage.py migrate

:: Create superuser
echo Creating superuser...
python manage.py createsuperuser

:: All done
cd ..
echo ===========================================
echo Setup complete!
echo 1. To start the server: cd backend && python manage.py runserver
echo 2. Open your browser and go to: http://127.0.0.1:8000/
echo ===========================================
