import io
import logging
from typing import Dict, Any, Tuple
from PIL import Image

from app.services.yolo_service import YOLOService
from app.utils.image_utils import base64_to_image, image_to_base64
from app.utils.storage import ImageStorage
from app.utils.cache import ImageCache

class PredictionService:
    def __init__(self, yolo_service: YOLOService, storage: ImageStorage, cache: ImageCache):
        self.logger = logging.getLogger(__name__)
        self.yolo_service = yolo_service
        self.storage = storage
        self.cache = cache
    
    def predict(self, user_id: str, image_base64: str) -> Dict[str, Any]:
        try:
            self.logger.info(f"Processing prediction for user: {user_id}")
            
            image = base64_to_image(image_base64)
            result = self.yolo_service.predict(image)
            
            filename = self.storage.generate_filename(user_id)
            
            image_bytes = io.BytesIO()
            result['image'].save(image_bytes, format='JPEG')
            image_bytes.seek(0)
            image_data = image_bytes.read()
            
            self.storage.save_image(user_id, image_data, filename)
            
            self.cache.set((user_id, filename), image_data)
            
            result_base64 = image_to_base64(result['image'])
            
            return {
                'boxes': result['boxes'],
                'image': result_base64,
                'filename': filename
            }
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            raise
    
    def get_latest_image(self, user_id: str) -> Tuple[str, bytes]:
        try:
            cached = self.cache.get_latest(user_id)
            if cached:
                self.logger.debug(f"Returning cached image for user: {user_id}")
                return cached
            
            self.logger.info(f"Fetching latest image from storage for user: {user_id}")
            filename, image_bytes = self.storage.get_latest_image(user_id)
            self.cache.set((user_id, filename), image_bytes)
            return filename, image_bytes
        except FileNotFoundError:
            self.logger.warning(f"No images found for user: {user_id}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to get latest image: {e}")
            raise
    
    def get_image_history(self, user_id: str) -> list:
        try:
            return self.storage.get_image_history(user_id)
        except Exception as e:
            self.logger.error(f"Failed to get image history: {e}")
            raise
    
    def delete_image(self, user_id: str, filename: str) -> bool:
        try:
            self.cache.delete((user_id, filename))
            return self.storage.delete_image(user_id, filename)
        except Exception as e:
            self.logger.error(f"Failed to delete image: {e}")
            raise
    
    def get_image(self, user_id: str, filename: str) -> bytes:
        try:
            cached = self.cache.get((user_id, filename))
            if cached:
                self.logger.debug(f"Returning cached image: {filename}")
                return cached
            
            self.logger.info(f"Fetching image from storage: {filename}")
            filepath = self.storage.get_image_path(user_id, filename)
            with open(filepath, 'rb') as f:
                image_bytes = f.read()
            
            self.cache.set((user_id, filename), image_bytes)
            return image_bytes
        except Exception as e:
            self.logger.error(f"Failed to get image: {e}")
            raise
