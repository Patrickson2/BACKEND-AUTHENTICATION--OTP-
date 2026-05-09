#!/bin/bash
echo "Restarting backend server with CORS fix..."

# Kill existing backend processes
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "python.*main.py" 2>/dev/null || true
sleep 2

# Start backend with proper CORS
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

echo "Backend restarted with CORS enabled"
echo "Frontend should now be able to connect to http://localhost:8001"
