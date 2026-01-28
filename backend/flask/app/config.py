import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
    
    FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 5001))
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    IMAGE_SAVE_DIR = os.path.join(BASE_DIR, 'static', 'drone_images')
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    
    MAX_CACHE_SIZE = 100
    CACHE_TTL = 3600
    
    YOLO_MODEL_PATH = os.environ.get('YOLO_MODEL_PATH', '../../weights/best.pt')
    YOLO_IMG_SIZE = 320
    YOLO_CONF = 0.3
    YOLO_IOU = 0.5
    
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'flask.log')
    
    @staticmethod
    def init_app(app):
        os.makedirs(Config.IMAGE_SAVE_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
