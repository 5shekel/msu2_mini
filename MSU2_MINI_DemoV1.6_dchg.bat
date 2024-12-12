@echo off
cd /D "%~dp0"
set "BASEDIR=%cd%"

python.exe %BASEDIR%\MSU2_MINI_DemoV1.6_dchg.py
if not errorlevel 0 (
    echo "An error occurred!"
    pause
)
