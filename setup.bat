@echo off
echo ========================================================
echo    🎭 Playwright Practice Studio - Automated Setup
echo ========================================================
echo.

echo [1/3] Installing Python Dependencies (FastAPI, Uvicorn, Playwright)...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Python dependencies installation failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/3] Installing Node.js & TypeScript Dependencies...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] npm install failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/4] Installing Python Playwright Chromium Browser...
python -m playwright install chromium
if %errorlevel% neq 0 (
    echo [WARNING] Playwright browser install reported an issue, continuing...
)

echo.
echo [4/4] Installing Node.js Playwright Chromium Browser...
call npx playwright install chromium
if %errorlevel% neq 0 (
    echo [WARNING] Node.js Playwright browser install reported an issue, continuing...
)

echo.
echo ========================================================
echo    🎉 Setup Complete! You can now run start.bat
echo ========================================================
pause
