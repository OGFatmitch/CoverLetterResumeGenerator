#!/bin/bash

# Function to handle cleanup on script exit
cleanup() {
    echo "Shutting down servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap to catch script termination
trap cleanup EXIT

# Start the backend server
echo "Starting backend server..."
cd src
python -m uvicorn main:app --reload &
BACKEND_PID=$!

# Wait a moment for the backend to start
sleep 2

# Start the frontend server
echo "Starting frontend server..."
cd ../frontend
streamlit run app.py &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 