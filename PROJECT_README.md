# YOLO Drone Obstacle Avoidance System

A comprehensive full-stack system for autonomous drone obstacle detection and avoidance using YOLOv11.

## System Architecture

This system consists of three main components:

1. **Flask Backend** - YOLOv11 inference service for real-time obstacle detection
2. **SpringBoot Backend** - REST API for drone management, user management, and system control
3. **Vue.js Frontend** - Web interface for monitoring, controlling, and analyzing the drone system

## Technology Stack

- **Frontend**: Vue 3, Element Plus, Vue Router, Axios
- **Backend**: SpringBoot 3.1.5, JPA, MySQL
- **AI/ML**: YOLOv11, Flask, OpenCV, Ultralytics
- **Database**: MySQL 8.0

## Project Structure

```
-YOLOv11-/
├── backend/
│   ├── flask/                 # Flask YOLO inference service
│   │   ├── app.py            # Flask application with /predict endpoint
│   │   └── requirements.txt   # Python dependencies
│   └── springboot/           # SpringBoot REST API
│       ├── pom.xml           # Maven configuration
│       └── src/
│           └── main/
│               ├── java/com/yolo/drone/
│               │   ├── entity/      # JPA entities
│               │   ├── repository/  # Data repositories
│               │   ├── service/     # Business logic
│               │   ├── controller/  # REST controllers
│               │   └── config/      # Configuration
│               └── resources/
│                   └── application.properties
├── frontend/
│   └── vue/                  # Vue.js frontend
│       ├── package.json
│       ├── vite.config.js
│       ├── index.html
│       └── src/
│           ├── main.js
│           ├── App.vue
│           ├── router/
│           ├── views/
│           ├── components/
│           └── api/
├── database/
│   └── schema.sql            # Database schema
└── weights/
    └── best.pt              # YOLOv11 model weights
```

## Setup Instructions

### Prerequisites

- Java 17 or higher
- Python 3.8 or higher
- Node.js 16 or higher
- MySQL 8.0 or higher
- Maven 3.6 or higher

### Database Setup

1. Create MySQL database and run the schema:

```bash
mysql -u root -p < database/schema.sql
```

2. Update database credentials in `backend/springboot/src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/yolo?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true
spring.datasource.username=root
spring.datasource.password=your_password
```

### Flask Backend Setup

1. Navigate to the Flask directory:

```bash
cd backend/flask
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the Flask server:

```bash
python app.py
```

The Flask server will start on `http://localhost:5001`

### SpringBoot Backend Setup

1. Navigate to the SpringBoot directory:

```bash
cd backend/springboot
```

2. Build the project using Maven:

```bash
mvn clean install
```

3. Run the SpringBoot application:

```bash
mvn spring-boot:run
```

The SpringBoot server will start on `http://localhost:8080`

### Vue.js Frontend Setup

1. Navigate to the Vue directory:

```bash
cd frontend/vue
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The Vue application will start on `http://localhost:5173`

## API Endpoints

### Flask Endpoints

- `POST /predict` - YOLO inference endpoint
  - Request: `{ userId, image (base64), token }`
  - Response: `{ code, message, data: { boxes, image } }`

### SpringBoot Endpoints

- `POST /api/upload` - Upload image and get prediction
- `POST /api/droneInfo` - Get single drone status
- `POST /api/alldroneInfo` - Get all drones status
- `POST /api/userInfo` - Get all users
- `DELETE /api/deleteUser` - Delete user
- `PUT /api/updateUser` - Update user
- `POST /api/createUser` - Create user

## Frontend Pages

- `/` - Home page with drone status overview
- `/flying` - Live drone monitoring with YOLO predictions
- `/login` - User login and registration
- `/control/drone` - Drone control panel (admin only)
- `/control/user` - User management (admin only)
- `/analyze` - System analytics and statistics

## Features

1. **Real-time Obstacle Detection** - YOLOv11-based detection with bounding boxes
2. **Drone Status Monitoring** - Track drone positions, status, and tasks
3. **User Management** - Admin panel for managing users and permissions
4. **Control Panel** - Manual/automatic mode switching for drones
5. **Analytics Dashboard** - Visual statistics and performance metrics
6. **Task Management** - Track completed tasks and drone performance

## Database Schema

### Tables

- **user** - User accounts and roles
- **drone** - Drone status and task information
- **work_list** - Task assignments and tracking
- **control_log** - Operation history and audit trail

## Usage

1. Start all three services (Flask, SpringBoot, Vue)
2. Open browser to `http://localhost:5173`
3. Login or register an account
4. Monitor drones, upload images for prediction, or control drones (admin)

## Troubleshooting

### Flask Server Issues

- Ensure YOLO model weights (`best.pt`) are in the `weights/` directory
- Check Python dependencies are installed correctly

### SpringBoot Issues

- Verify MySQL is running and credentials are correct
- Check port 8080 is not in use

### Vue.js Issues

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 5173 is available

## License

This project is for educational and research purposes.

## Contact

For questions or issues, please refer to the project documentation.
