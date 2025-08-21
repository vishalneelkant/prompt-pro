@echo off
echo 🚀 Starting Prompt Optimizer Application...
echo.

REM Check if .env file exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please create a .env file with your API keys:
    echo PINECONE=your_pinecone_api_key
    echo OPENAI_API_KEY=your_openai_api_key
    pause
    exit /b 1
)

echo 📦 Checking Python dependencies...
python -c "import flask, pinecone, langchain_openai" 2>nul
if errorlevel 1 (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

echo 📦 Checking Node.js dependencies...
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

echo.
echo ✅ Dependencies ready!
echo.
echo 🌐 Starting Backend API on http://localhost:5000
echo 🎨 Starting Frontend on http://localhost:3000
echo.
echo Press Ctrl+C to stop both services
echo.

REM Start backend
start "Backend API" python api.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
start "Frontend" npm start

echo.
echo 🎉 Both services are starting!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause
