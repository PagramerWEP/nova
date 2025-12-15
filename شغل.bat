@echo off
chcp 65001 >nul
cd backend
python manage.py runserver 0.0.0.0:8080
pause
