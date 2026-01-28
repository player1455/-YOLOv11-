import os
import time
import threading
from typing import Tuple, Optional

class ImageCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.latest_cache = {}
        self.lock = threading.Lock()
        self.max_size = max_size
    
    def get(self, key: Tuple[str, str]) -> Optional[bytes]:
        with self.lock:
            return self.cache.get(key)
    
    def get_latest(self, user_id: str) -> Optional[Tuple[str, bytes]]:
        with self.lock:
            return self.latest_cache.get(user_id)
    
    def set(self, key: Tuple[str, str], value: bytes):
        with self.lock:
            self.cache[key] = value
            user_id = key[0]
            self.latest_cache[user_id] = (key[1], value)
            
            if len(self.cache) > self.max_size:
                old_keys = list(self.cache.keys())[:len(self.cache) - self.max_size]
                for old_key in old_keys:
                    self.cache.pop(old_key, None)
    
    def delete(self, key: Tuple[str, str]):
        with self.lock:
            self.cache.pop(key, None)
            user_id = key[0]
            if user_id in self.latest_cache:
                latest_filename, _ = self.latest_cache[user_id]
                if latest_filename == key[1]:
                    self.latest_cache.pop(user_id, None)
    
    def clear_user(self, user_id: str):
        with self.lock:
            keys_to_remove = [k for k in self.cache.keys() if k[0] == user_id]
            for key in keys_to_remove:
                self.cache.pop(key, None)
            self.latest_cache.pop(user_id, None)
    
    def clear_all(self):
        with self.lock:
            self.cache.clear()
            self.latest_cache.clear()
