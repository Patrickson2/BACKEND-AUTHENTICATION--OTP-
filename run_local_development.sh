#!/bin/bash
echo "🚀 Starting OTP Authentication System - Local Development"
echo ""

# Kill any existing processes
echo "🔄 Stopping existing processes..."
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "npm.*dev" 2>/dev/null || true
sleep 2

# Start backend server
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload &
BACKEND_PID=$!

echo "✅ Backend started with PID: $BACKEND_PID"
echo "🌐 Backend URL: http://localhost:8001"
echo "📚 API Docs: http://localhost:8001/docs"
echo ""

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server..."
cd ../frontend/Login-OTP
npm run dev &
FRONTEND_PID=$!

echo "✅ Frontend started with PID: $FRONTEND_PID"
echo "🌐 Frontend URL: http://localhost:5173"
echo ""

echo "🎉 Application is running locally!"
echo ""
echo "📊 Services Status:"
echo "   Backend: http://localhost:8001 (PID: $BACKEND_PID)"
echo "   Frontend: http://localhost:5173 (PID: $FRONTEND_PID)"
echo ""
echo "🛑 To stop: kill $BACKEND_PID $FRONTEND_PID"
echo "📱 Test URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo "   Email Test: http://localhost:8001/api/debug/test-email"
echo ""
echo "🔧 Test SendGrid:"
echo "   cd backend && source venv/bin/activate"
echo "   python -c 'from lib.sendgrid_service import sendgrid_service; sendgrid_service.send_otp_email(\"your@email.com\", \"123456\", \"TestUser\")'"
echo ""
echo "⚠️  Don't forget to:"
echo "   1. Update backend/.env with your SendGrid API key"
echo "   2. Test the complete registration flow"
echo "   3. Check email delivery (console + real email)"
