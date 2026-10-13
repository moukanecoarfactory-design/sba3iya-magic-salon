@echo off
title Sba3iya Magic Salon
cd /d "%~dp0"

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERREUR : Python n'est pas installe
    echo ========================================
    echo.
    echo Veuillez installer Python depuis :
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT : cochez "Add Python to PATH"
    echo.
    pause
    exit /b
)

REM Lancer l'application
start "" pythonw main.py
exit