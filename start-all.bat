@echo off
echo Starting YOLO Drone Obstacle Avoidance System...
echo.

echo Step 1: Starting Flask Backend (YOLO Inference Service)...
start "Flask Backend" cmd /k "cd backend\flask && venv\Scripts\activate && python app.py"
timeout /t 3 /nobreak >nul

echo Step 2: Starting SpringBoot Backend (REST API)...
start "SpringBoot Backend" cmd /k "cd backend\springboot && mvn spring-boot:run"
timeout /t 5 /nobreak >nul

echo Step 3: Starting Vue.js Frontend...
start "Vue Frontend" cmd /k "cd frontend\vue && npm run dev"

echo.
echo All services are starting...
echo.
echo Access the application at: http://localhost:5173
echo Flask API: http://localhost:5001
echo SpringBoot API: http://localhost:8080
echo.
pause
