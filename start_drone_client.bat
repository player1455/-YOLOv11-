@echo off
echo ========================================
echo Starting Drone Login Client...
echo ========================================
echo.
echo This client will:
echo   1. Login to the system
echo   2. Capture images from camera
echo   3. Upload images for YOLO detection
echo   4. Receive obstacle avoidance commands
echo.
echo Account: test_drone_user / test123
echo.
echo Press Ctrl+C to stop the client
echo ========================================
echo.

python drone_login_client.py

echo.
echo ========================================
echo Drone client stopped
echo ========================================
pause
