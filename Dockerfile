# Multi-stage build for frontend and backend
FROM node:20-alpine AS frontend-build

# Set working directory for frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/Login-OTP/package*.json ./

# Install frontend dependencies
RUN npm ci

# Copy frontend source code
COPY frontend/Login-OTP/ .

# Force cache invalidation and build frontend
RUN touch /app/frontend/.build-cache-bust && npm run build

# Backend stage
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist ./static

# Create database directory
RUN mkdir -p /app/data

# The app runs on port 8000
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./data/auth_system.db

# Start the FastAPI server
CMD ["python", "main.py"]
