import os
import time
import glob
from typing import List, Tuple
from pathlib import Path

class ImageStorage:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def get_user_dir(self, user_id: str) -> Path:
        user_dir = self.base_dir / user_id
        user_dir.mkdir(exist_ok=True)
        return user_dir
    
    def save_image(self, user_id: str, image_bytes: bytes, filename: str) -> str:
        user_dir = self.get_user_dir(user_id)
        filepath = user_dir / filename
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        return str(filepath)
    
    def get_image_path(self, user_id: str, filename: str) -> str:
        user_dir = self.get_user_dir(user_id)
        filepath = user_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Image not found: {filepath}")
        return str(filepath)
    
    def get_latest_image(self, user_id: str) -> Tuple[str, bytes]:
        user_dir = self.get_user_dir(user_id)
        image_files = list(user_dir.glob("*.jpg"))
        
        if not image_files:
            raise FileNotFoundError(f"No images found for user: {user_id}")
        
        latest_file = max(image_files, key=lambda f: f.stat().st_mtime)
        filename = latest_file.name
        
        with open(latest_file, 'rb') as f:
            image_bytes = f.read()
        
        return filename, image_bytes
    
    def get_image_history(self, user_id: str) -> List[str]:
        user_dir = self.get_user_dir(user_id)
        if not user_dir.exists():
            return []
        
        image_files = list(user_dir.glob("*.jpg"))
        image_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        return [f.name for f in image_files]
    
    def delete_image(self, user_id: str, filename: str) -> bool:
        try:
            user_dir = self.get_user_dir(user_id)
            filepath = user_dir / filename
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception:
            return False
    
    def delete_user_images(self, user_id: str) -> int:
        user_dir = self.get_user_dir(user_id)
        if not user_dir.exists():
            return 0
        
        image_files = list(user_dir.glob("*.jpg"))
        count = len(image_files)
        for filepath in image_files:
            filepath.unlink()
        
        return count
    
    def generate_filename(self, user_id: str) -> str:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        milliseconds = int(time.time() * 1000) % 1000
        timestamp_with_ms = f"{timestamp}_{milliseconds:03d}"
        return f"{user_id}_{timestamp_with_ms}.jpg"
