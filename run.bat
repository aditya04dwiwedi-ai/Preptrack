@echo off
title Placement Preparation & Tracking System - AKTU Mini Project
echo ======================================================================
echo  PLACEMENT PREPARATION ^& TRACKING SYSTEM
echo  Department of Computer Science ^& Engineering - AIML
echo  Lloyd Institute of Engineering ^& Technology, Greater Noida
echo  Affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU)
echo ======================================================================
echo.
echo Starting Flask Web Application Server...
echo (If PrepBot shows an error, read the [PrepBot] lines in this window.)
echo.

where python >nul 2>nul
if %errorlevel%==0 (set PY=python) else (set PY=py)

%PY% -m pip install -q -r requirements.txt

REM Open the browser a few seconds AFTER the server starts (opening it first shows "can't connect")
start "" /min cmd /c "timeout /t 4 /nobreak >nul & start "" http://127.0.0.1:5000"
%PY% app.py

pause
