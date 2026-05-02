@echo off
setlocal

cd /d "%~dp0"

where uv >nul 2>nul
if errorlevel 1 (
    echo Missing uv.
    echo Install uv or run this project in an environment where uv is available.
    pause
    exit /b 1
)

if "%PYGM_PYTHON%"=="" (
    set "PYGM_PYTHON=python"
)

uv run --python "%PYGM_PYTHON%" pyinstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --console ^
    --name pygm ^
    --paths src ^
    "src\pygm\__main__.py"

if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)

if exist "pygm.env" (
    copy /Y "pygm.env" "dist\pygm.env" >nul
)

echo Built dist\pygm.exe
echo Start dist\pygm.exe to open the AI chat console.
pause
