@echo off
setlocal

set "CURRENT_DIR=%cd%"
for %%i in ("%CURRENT_DIR%") do set "PARENT_DIR=%%~dpi"
set "PARENT_DIR=%PARENT_DIR:~0,-1%"
set "PYTHONPATH=%PARENT_DIR%;%CURRENT_DIR%;%PYTHONPATH%"
uvicorn app:app --reload

endlocal
