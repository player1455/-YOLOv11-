import requests
import asyncio
import aiohttp
import base64
import cv2
import numpy as np
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class DroneStatus(Enum):
    IDLE = "idle"
    FLYING = "flying"
    ERROR = "error"

@dataclass
class DroneConfig:
    base_url: str
    username: str
    password: str
    drone_id: str
    camera_index: int = 0
    image_quality: int = 70
    send_interval: float = 0.5
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 10.0

class DroneClient:
    def __init__(self, config: DroneConfig):
        self.config = config
        self.token: Optional[str] = None
        self.logged_in = False
        self.status = DroneStatus.IDLE
        self.cap = None
        self.running = False
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(f'DroneClient_{self.config.drone_id}')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def login(self) -> bool:
        for attempt in range(self.config.max_retries):
            try:
                self.logger.info(f"Login attempt {attempt + 1}/{self.config.max_retries}")
                response = requests.post(
                    f"{self.config.base_url}/login",
                    json={
                        'username': self.config.username,
                        'password': self.config.password
                    },
                    timeout=self.config.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("code") == 200:
                        self.token = result.get("data", {}).get("token")
                        self.logged_in = True
                        self.logger.info("Login successful")
                        return True
                
                self.logger.warning(f"Login failed: {response.text}")
                
            except requests.exceptions.Timeout:
                self.logger.error(f"Login timeout (attempt {attempt + 1})")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Login error: {e}")
            
            if attempt < self.config.max_retries - 1:
                time.sleep(self.config.retry_delay)
        
        self.status = DroneStatus.ERROR
        return False
    
    def capture_from_camera(self) -> Optional[str]:
        try:
            if self.cap is None:
                self.cap = cv2.VideoCapture(self.config.camera_index)
                if not self.cap.isOpened():
                    self.logger.error("Failed to open camera")
                    return None
            
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Failed to capture frame")
                return None
            
            _, img_encoded = cv2.imencode('.jpg', frame, 
                [int(cv2.IMWRITE_JPEG_QUALITY), self.config.image_quality])
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')
            return img_base64
            
        except Exception as e:
            self.logger.error(f"Camera capture error: {e}")
            return None
    
    async def async_send_image(self, session: aiohttp.ClientSession, 
                             image_base64: str) -> Optional[Dict[str, Any]]:
        if not self.token:
            self.logger.error("No token available")
            return None
        
        payload = {
            "userId": self.config.drone_id,
            "image": f"data:image/jpeg;base64,{image_base64}",
            "token": self.token,
            "timestamp": str(int(time.time() * 1000))
        }
        
        for attempt in range(self.config.max_retries):
            try:
                async with session.post(
                    f"{self.config.base_url}/upload",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get("code") == 200:
                            self._process_command(result.get("data", {}))
                            return result.get("data")
                    else:
                        self.logger.warning(f"Upload failed: {await response.text()}")
                    
            except asyncio.TimeoutError:
                self.logger.error(f"Upload timeout (attempt {attempt + 1})")
            except aiohttp.ClientError as e:
                self.logger.error(f"Upload error: {e}")
            
            if attempt < self.config.max_retries - 1:
                await asyncio.sleep(self.config.retry_delay)
        
        return None
    
    def _process_command(self, data: Dict[str, Any]):
        if data.get("is_control"):
            control = data.get("control")
            position = data.get("position")
            self.logger.info(f"Control command: {control} at {position}")
    
    async def start_continuous_send(self):
        if not self.logged_in:
            self.logger.error("Not logged in")
            return
        
        self.running = True
        self.status = DroneStatus.FLYING
        self.logger.info("Starting continuous image sending")
        
        async with aiohttp.ClientSession() as session:
            while self.running:
                try:
                    image_base64 = self.capture_from_camera()
                    if image_base64:
                        await self.async_send_image(session, image_base64)
                    
                    await asyncio.sleep(self.config.send_interval)
                    
                except Exception as e:
                    self.logger.error(f"Continuous send error: {e}")
                    await asyncio.sleep(self.config.retry_delay)
        
        self.status = DroneStatus.IDLE
        self.logger.info("Continuous sending stopped")
    
    def stop_continuous_send(self):
        self.running = False
        self.logger.info("Stopping continuous image sending")
    
    def start_sync_continuous_send(self):
        import threading
        self.running = True
        self.status = DroneStatus.FLYING
        
        def send_loop():
            while self.running:
                try:
                    image_base64 = self.capture_from_camera()
                    if image_base64:
                        asyncio.run(self.async_send_image(
                            aiohttp.ClientSession(), image_base64
                        ))
                    time.sleep(self.config.send_interval)
                except Exception as e:
                    self.logger.error(f"Sync send error: {e}")
                    time.sleep(self.config.retry_delay)
        
        thread = threading.Thread(target=send_loop, daemon=True)
        thread.start()
        self.logger.info("Started sync continuous sending")
    
    def cleanup(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.logger.info("Cleanup completed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
