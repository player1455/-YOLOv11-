#!/bin/bash

echo "Starting YOLO Drone System..."

cd backend/flask
echo "Starting Flask YOLO service on port 5001..."
waitress-serve --listen=0.0.0.0:5001 --threads=10 wsgi:app &
FLASK_PID=$!

cd ../springboot
echo "Starting Spring Boot service on port 8080..."
mvn spring-boot:run &
SPRING_PID=$!

cd ../../frontend/vue
echo "Starting Vue frontend on port 5173..."
npm run dev &
VUE_PID=$!

echo "All services started!"
echo "Flask PID: $FLASK_PID"
echo "Spring Boot PID: $SPRING_PID"
echo "Vue PID: $VUE_PID"

wait
