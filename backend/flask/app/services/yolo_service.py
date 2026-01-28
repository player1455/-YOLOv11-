from ultralytics import YOLO
import logging
from typing import List, Dict, Any
from PIL import Image
import numpy as np
import cv2

class YOLOService:
    def __init__(self, model_path: str, img_size: int = 320, conf: float = 0.3, iou: float = 0.5):
        self.logger = logging.getLogger(__name__)
        self.model_path = model_path
        self.img_size = img_size
        self.conf = conf
        self.iou = iou
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            self.logger.info(f"Loading YOLO model from {self.model_path}")
            self.model = YOLO(self.model_path)
            self.logger.info("YOLO model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load YOLO model: {e}")
            raise
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        try:
            img_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            results = self.model.predict(
                source=img_np,
                imgsz=self.img_size,
                conf=self.conf,
                iou=self.iou,
                save=False,
                verbose=False
            )
            
            plotted_bgr = results[0].plot()
            plotted_rgb = cv2.cvtColor(plotted_bgr, cv2.COLOR_BGR2RGB)
            result_image = Image.fromarray(plotted_rgb)
            
            boxes = self._extract_boxes(results[0])
            
            return {
                'boxes': boxes,
                'image': result_image
            }
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            raise
    
    def _extract_boxes(self, result) -> List[Dict[str, Any]]:
        boxes = []
        if result.boxes is not None:
            for box in result.boxes:
                boxes.append({
                    'xyxy': box.xyxy.tolist()[0],
                    'confidence': float(box.conf),
                    'class': int(box.cls),
                    'class_name': self.model.names[int(box.cls)]
                })
        return boxes
    
    def get_class_names(self) -> Dict[int, str]:
        return self.model.names if self.model else {}
