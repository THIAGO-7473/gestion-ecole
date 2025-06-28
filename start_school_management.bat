@echo off
cd /d E:\school_management
call venv\Scripts\activate
cls
echo Environnement activé ! Lancement du serveur et Cursor...
start "" "C:\Users\Ir. THIAGO\AppData\Local\Programs\cursor\Cursor.exe".
python manage.py runserver
pause
