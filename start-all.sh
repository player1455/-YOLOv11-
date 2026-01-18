#!/bin/bash

echo "Starting YOLO Drone Obstacle Avoidance System..."
echo ""

echo "Step 1: Starting Flask Backend (YOLO Inference Service)..."
cd backend/flask
source venv/bin/activate
python app.py &
FLASK_PID=$!
cd ../..
sleep 3

echo "Step 2: Starting SpringBoot Backend (REST API)..."
cd backend/springboot
mvn spring-boot:run &
SPRING_PID=$!
cd ../..
sleep 5

echo "Step 3: Starting Vue.js Frontend..."
cd frontend/vue
npm run dev &
VUE_PID=$!
cd ../..

echo ""
echo "All services are starting..."
echo ""
echo "Access the application at: http://localhost:5173"
echo "Flask API: http://localhost:5001"
echo "SpringBoot API: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all services"

trap "kill $FLASK_PID $SPRING_PID $VUE_PID" EXIT

wait
