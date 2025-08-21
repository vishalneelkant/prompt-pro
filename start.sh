#!/bin/bash

echo "🚀 Starting Prompt Optimizer Application..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "PINECONE=your_pinecone_api_key"
    echo "OPENAI_API_KEY=your_openai_api_key"
    exit 1
fi

# Check if Python dependencies are installed
echo "📦 Checking Python dependencies..."
if ! python -c "import flask, pinecone, langchain_openai" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Check if Node.js dependencies are installed
echo "📦 Checking Node.js dependencies..."
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo ""
echo "✅ Dependencies ready!"
echo ""
echo "🌐 Starting Backend API on http://localhost:5000"
echo "🎨 Starting Frontend on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Start backend in background
python api.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
npm start &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for both processes
wait
