@echo off
echo ========================================
echo Starting YOLO Drone System...
echo ========================================
echo.

cd backend\flask
echo [1/3] Starting Flask YOLO service on port 5001...
start "Flask Service" /min cmd /k "waitress-serve --listen=127.0.0.1:5001 --threads=10 wsgi:app"
timeout /t 5 /nobreak > nul

cd ..\springboot
echo [2/3] Starting Spring Boot service on port 8080...
start "Spring Boot Service" /min cmd /k "mvn spring-boot:run"
timeout /t 10 /nobreak > nul

cd ..\..\frontend\vue
echo [3/3] Starting Vue frontend on port 5174...
start "Vue Frontend" /min cmd /k "npm run dev"

echo.
echo ========================================
echo All services started successfully!
echo ========================================
echo.
echo Service URLs:
echo   - Flask YOLO:  http://localhost:5001
echo   - Spring Boot:  http://localhost:8080
echo   - Vue Frontend: http://localhost:5174
echo.
echo Available Test Accounts:
echo   - Drone: test_drone / 123456
echo   - Admin: admin / admin123
echo.
echo Press any key to close this window...
pause > nul
