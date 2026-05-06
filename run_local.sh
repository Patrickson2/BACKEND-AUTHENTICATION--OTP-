#!/bin/bash
echo "🚀 Starting OTP Authentication System Locally"
echo ""

# Kill any existing processes
echo "🔄 Stopping existing processes..."
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
sleep 2

# Start backend server
echo "🔧 Starting backend server..."
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "✅ Backend started with PID: $BACKEND_PID"
echo "🌐 Backend URL: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server..."
cd frontend/Login-OTP
npm run dev &
FRONTEND_PID=$!

echo "✅ Frontend started with PID: $FRONTEND_PID"
echo "🌐 Frontend URL: http://localhost:5173"
echo ""

echo "🎉 Application is running locally!"
echo ""
echo "📊 Services Status:"
echo "   Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo "   Frontend: http://localhost:5173 (PID: $FRONTEND_PID)"
echo ""
echo "🛑 To stop: kill $BACKEND_PID $FRONTEND_PID"
echo "📱 Test URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Email Test: http://localhost:8000/api/debug/test-email"
