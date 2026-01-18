import os
import time
from PIL import Image
import numpy as np
import cv2

# 图片保存目录
IMAGE_SAVE_DIR = "static/drone_images"
user_id = "drone001"

# 确保保存目录存在
user_image_dir = os.path.join(IMAGE_SAVE_DIR, user_id)
os.makedirs(user_image_dir, exist_ok=True)

# 创建一张简单的测试图片
img = np.zeros((200, 200, 3), dtype=np.uint8)
cv2.rectangle(img, (50, 50), (150, 150), (0, 255, 0), 2)
cv2.putText(img, "Test Image", (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# 转换为PIL Image
result_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# 使用时间戳作为文件名
timestamp = time.strftime("%Y%m%d_%H%M%S")
milliseconds = int(time.time() * 1000) % 1000
timestamp_with_ms = f"{timestamp}_{milliseconds:03d}"
filename = f"{user_id}_{timestamp_with_ms}.jpg"
filepath = os.path.join(user_image_dir, filename)

# 保存图片
result_image.save(filepath)
print(f"Image saved to: {filepath}")

# 检查文件是否存在
if os.path.exists(filepath):
    print(f"Image exists at: {filepath}")
    print(f"File size: {os.path.getsize(filepath)} bytes")
else:
    print(f"ERROR: Image not saved at: {filepath}")
