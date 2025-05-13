# STOP SERVERS
# deactivate

# chmod +x deploy.sh
# ./deploy.sh


#!/bin/bash

# Stop current running services
echo "===== Stopping running services ====="
echo "Stopping Django Server if running..."
pkill -f runserver
echo "Stopping any running Node.js processes..."
pkill -f node
echo "Services stopped."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "===== Activating virtual environment ====="
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "Virtual environment not found, creating new one..."
python3 -m venv venv
source venv/bin/activate
    fi
fi

# Install or update dependencies
echo "===== Installing dependencies ====="
echo "Installing Python packages..."
pip install -r requirements.txt

echo "Installing Node.js packages..."
npm install

# Run migrations
echo "===== Running database migrations ====="
python manage.py makemigrations
python manage.py migrate

# Start Django server
echo "===== Starting Django server ====="
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait for Django server to start up
echo "Waiting for Django server to start up..."
sleep 5

# Check if Django server is running
if ps -p $DJANGO_PID > /dev/null; then
    echo "Django server started successfully (PID: $DJANGO_PID)"
    
    # Start frontend server
    echo "===== Starting frontend server ====="
    if [ -d "frontend" ]; then
        cd frontend
        npm run serve &
        FRONTEND_PID=$!
        cd ..
        echo "Frontend server started (PID: $FRONTEND_PID)"
    else
        echo "Frontend directory not found, skipping frontend server start."
    fi
    
    echo "===== Deployment complete ====="
    echo "Django server running at: http://localhost:8000"
    echo "Frontend server running at: http://localhost:8080 (if applicable)"
    echo "Press Ctrl+C to stop all servers"
    
    # Keep script running until Ctrl+C
    wait $DJANGO_PID
else
    echo "Django server failed to start. Please check logs for details."
    exit 1
fi
