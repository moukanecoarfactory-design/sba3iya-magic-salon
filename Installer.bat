@echo off
title Installation - Sba3iya Magic Salon
color 0E
cd /d "%~dp0"

echo.
echo ========================================
echo   SBA3IYA MAGIC SALON - Installation
echo ========================================
echo.

REM Vérifier Python
echo [1/3] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo    ERREUR : Python n'est pas installe !
    echo.
    echo    Telechargez Python sur :
    echo      https://www.python.org/downloads/
    echo.
    echo    IMPORTANT : Pendant l'installation,
    echo    cochez "Add Python to PATH"
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b
)
echo    OK - Python detecte
echo.

REM Installer les dependances
echo [2/3] Installation des composants (2-3 minutes)...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet customtkinter pillow
if errorlevel 1 (
    echo    ERREUR lors de l'installation
    pause
    exit /b
)
echo    OK - Composants installes
echo.

REM Initialiser la base
echo [3/3] Initialisation de la base de donnees...
python -c "import database as db; db.initialiser_bdd(); db.inserer_donnees_defaut(); print('   OK - Base prete')"
echo.

echo ========================================
echo   INSTALLATION TERMINEE !
echo ========================================
echo.
echo Pour lancer l'application :
echo   Double-cliquez sur "Lancer.bat"
echo.
echo Mot de passe Admin par defaut : admin123
echo.
pause