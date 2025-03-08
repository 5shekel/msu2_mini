@echo off
cd /D "%~dp0"

set "mainfilename=MSU2_MINI_DemoV1.6_dchg"
rem mkdir %mainfilename%.dist 2>nul

setlocal enabledelayedexpansion

for /f "delims=" %%i in ('where pyinstaller') do (
    set "pypath=%%~dpi"
)

rem --lto=yes
rem --standalone
rem --onefile
rem --windows-console-mode=disable
python -m nuitka --onefile --windows-console-mode=disable ^
	--enable-plugin=tk-inter --remove-output ^
	--include-data-files="%~dp0/resource/*"="resource/" ^
	--include-data-files="%pypath%../Lib/site-packages/HardwareMonitor/lib/*.dll"="HardwareMonitor/lib/" ^
	--windows-icon-from-ico=resource/icon.ico ^
	--output-filename=MSU2_mini.exe ^
	%mainfilename%.py

endlocal

set "datenow=%date:~5,2%%date:~8,2%"
set "outfilename=MSU2_MINI_MG(by nuitka£¨Œ»∂®≤ª±®∂æ)-%datenow%.exe"
move /Y MSU2_mini.exe "%outfilename%"

pause
