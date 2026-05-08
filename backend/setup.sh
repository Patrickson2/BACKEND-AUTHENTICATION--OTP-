#!/bin/bash
echo "🚀 Setting up OTP Authentication System Backend"
echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Initialize database
echo "🗄️ Initializing database..."
python init_database.py

echo "✅ Backend setup complete!"
echo ""
echo "🌐 To start the backend server:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "📚 To test SendGrid service:"
echo "   python -c 'from lib.sendgrid_service import sendgrid_service; sendgrid_service.test_connection()'"
