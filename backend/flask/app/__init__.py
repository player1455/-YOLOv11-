from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.utils.logger import setup_logger
from app.services.yolo_service import YOLOService
from app.services.prediction_service import PredictionService
from app.utils.storage import ImageStorage
from app.utils.cache import ImageCache
from app.routes import prediction_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    Config.init_app(app)
    
    CORS(app)
    
    logger = setup_logger('flask_app', Config.LOG_FILE, Config.LOG_LEVEL)
    app.logger = logger
    
    yolo_service = YOLOService(
        model_path=Config.YOLO_MODEL_PATH,
        img_size=Config.YOLO_IMG_SIZE,
        conf=Config.YOLO_CONF,
        iou=Config.YOLO_IOU
    )
    
    storage = ImageStorage(Config.IMAGE_SAVE_DIR)
    cache = ImageCache(max_size=Config.MAX_CACHE_SIZE)
    
    prediction_service = PredictionService(yolo_service, storage, cache)
    prediction_routes.init_prediction_service(prediction_service)
    
    from app.routes import register_blueprints
    register_blueprints(app)
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy', 'service': 'yolo-drone-api'})
    
    logger.info('Flask application created successfully')
    
    return app
