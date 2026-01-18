# Quick Start Guide

## Prerequisites Installation

### 1. Install Java 17
Download and install from: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html

### 2. Install Python 3.8+
Download and install from: https://www.python.org/downloads/

### 3. Install Node.js 16+
Download and install from: https://nodejs.org/

### 4. Install MySQL 8.0+
Download and install from: https://dev.mysql.com/downloads/mysql/

### 5. Install Maven
Download and install from: https://maven.apache.org/download.cgi

## Quick Setup (5 minutes)

### Step 1: Database Setup
```bash
# Open MySQL command line or tool
mysql -u root -p

# Run the schema script
source d:/codde/python/-YOLOv11-/database/schema.sql
```

### Step 2: Flask Backend Setup
```bash
cd backend/flask

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: SpringBoot Backend Setup
```bash
cd backend/springboot

# Update database password in src/main/resources/application.properties
# Change: spring.datasource.password=root to your MySQL password

# Build project
mvn clean install
```

### Step 4: Vue Frontend Setup
```bash
cd frontend/vue

# Install dependencies
npm install
```

## Running the System

### Option 1: Using Start Scripts (Recommended)

**Windows:**
```bash
start-all.bat
```

**Linux/Mac:**
```bash
chmod +x start-all.sh
./start-all.sh
```

### Option 2: Manual Start

**Terminal 1 - Flask:**
```bash
cd backend/flask
venv\Scripts\activate
python app.py
```

**Terminal 2 - SpringBoot:**
```bash
cd backend/springboot
mvn spring-boot:run
```

**Terminal 3 - Vue:**
```bash
cd frontend/vue
npm run dev
```

## Access the Application

Once all services are running:

- **Frontend**: http://localhost:5173
- **SpringBoot API**: http://localhost:8080
- **Flask API**: http://localhost:5001

## Default Users

The system comes with pre-configured users:

- **Admin**: username `admin001`, role `admin`
- **Drone 1**: username `drone001`, role `drone`
- **Drone 2**: username `drone002`, role `drone`
- **User 1**: username `user001`, role `user`

## Testing the System

1. Open http://localhost:5173 in your browser
2. Click "Login" and use any of the default users
3. Navigate to different pages:
   - Home: View all drones and statistics
   - Flying: Upload images for YOLO prediction
   - Control/Drone: Manage drone status (admin only)
   - Control/User: Manage users (admin only)
   - Analyze: View system analytics

## Troubleshooting

### Port Already in Use
If you see "port already in use" errors:

**Windows:**
```bash
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8080 | xargs kill -9
```

### Database Connection Error
- Verify MySQL is running
- Check credentials in `backend/springboot/src/main/resources/application.properties`
- Ensure database `yolo` exists

### Flask Model Not Found
- Ensure `weights/best.pt` file exists in the project root
- Download YOLOv11 model weights if missing

### Vue Build Errors
```bash
cd frontend/vue
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Customize the YOLO model with your own dataset
- Add more drone control features
- Implement real-time video streaming
- Add authentication and authorization
- Deploy to production servers

## Support

For detailed documentation, see [PROJECT_README.md](PROJECT_README.md)
