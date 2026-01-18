from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import base64
from ultralytics import YOLO
import io
import os
import time
import glob
import threading
import queue

app = Flask(__name__)
CORS(app)

model = YOLO("../../weights/best.pt")

# 图片保存目录
IMAGE_SAVE_DIR = "../../static/drone_images"

# 确保保存目录存在
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

# 图片缓存，key: (userId, filename), value: image bytes
image_cache = {}
# 缓存锁
cache_lock = threading.Lock()
# 最新图片缓存，key: userId, value: (filename, image_bytes)
latest_image_cache = {}
# 缓存大小限制
MAX_CACHE_SIZE = 50

# 视频流队列
video_streams = {}
# 视频流锁
stream_lock = threading.Lock()

def base64_to_image(base64_string):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'code': 400, 'message': 'No data provided'}), 400
        
        user_id = data.get('userId', 'drone001')
        image_data = data.get('image')
        token = data.get('token')
        
        if not image_data:
            return jsonify({'code': 400, 'message': 'Image data is required'}), 400
        
        image = base64_to_image(image_data)
        img_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        results = model.predict(source=img_np, imgsz=320, conf=0.3, iou=0.5, save=False)
        
        plotted_bgr = results[0].plot()
        plotted_rgb = cv2.cvtColor(plotted_bgr, cv2.COLOR_BGR2RGB)
        result_image = Image.fromarray(plotted_rgb)
        
        result_image_base64 = image_to_base64(result_image)
        
        boxes = []
        if results[0].boxes is not None:
            for box in results[0].boxes:
                boxes.append({
                    'xyxy': box.xyxy.tolist()[0],
                    'confidence': float(box.conf),
                    'class': int(box.cls),
                    'class_name': model.names[int(box.cls)]
                })
        
        # 保存检测后的图片到指定目录
        user_image_dir = os.path.join(IMAGE_SAVE_DIR, user_id)
        os.makedirs(user_image_dir, exist_ok=True)
        
        # 使用时间戳作为文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        milliseconds = int(time.time() * 1000) % 1000
        timestamp_with_ms = f"{timestamp}_{milliseconds:03d}"
        filename = f"{user_id}_{timestamp_with_ms}.jpg"
        filepath = os.path.join(user_image_dir, filename)
        result_image.save(filepath)
        
        # 缓存图片，提高后续访问速度
        with cache_lock:
            # 保存到普通缓存
            image_bytes = io.BytesIO()
            result_image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)
            image_cache[(user_id, filename)] = image_bytes.read()
            
            # 更新最新图片缓存
            latest_image_cache[user_id] = (filename, image_cache[(user_id, filename)])
            
            # 清理旧缓存，保持缓存大小在限制内
            if len(image_cache) > MAX_CACHE_SIZE:
                # 移除最早的缓存项
                old_keys = list(image_cache.keys())[:len(image_cache) - MAX_CACHE_SIZE]
                for key in old_keys:
                    image_cache.pop(key, None)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'boxes': boxes,
                'image': result_image_base64,
                'filename': filename
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/get_image_history', methods=['GET'])
def get_image_history():
    try:
        user_id = request.args.get('userId', 'drone001')
        user_image_dir = os.path.join(IMAGE_SAVE_DIR, user_id)
        
        if not os.path.exists(user_image_dir):
            return jsonify({
                'code': 200,
                'message': 'success',
                'data': {
                    'images': []
                }
            })
        
        # 获取所有图片文件，按时间顺序排序
        image_files = glob.glob(os.path.join(user_image_dir, "*.jpg"))
        image_files.sort(key=os.path.getmtime)
        
        # 提取文件名并构建URL
        images = [os.path.basename(f) for f in image_files]
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'images': images
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/delete_image', methods=['POST'])
def delete_image():
    try:
        data = request.get_json()
        user_id = data.get('userId', 'drone001')
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'code': 400, 'message': 'Filename is required'}), 400
        
        filepath = os.path.join(IMAGE_SAVE_DIR, user_id, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            # 从缓存中移除
            with cache_lock:
                cache_key = (user_id, filename)
                image_cache.pop(cache_key, None)
                # 如果是最新图片，也从最新图片缓存中移除
                if user_id in latest_image_cache:
                    latest_filename, _ = latest_image_cache[user_id]
                    if latest_filename == filename:
                        latest_image_cache.pop(user_id, None)
            return jsonify({'code': 200, 'message': 'success'})
        else:
            return jsonify({'code': 404, 'message': 'Image not found'}), 404
        
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/latest_image/<user_id>', methods=['GET'])
def get_latest_image(user_id):
    """获取最新的图片"""
    try:
        # 首先检查最新图片缓存
        with cache_lock:
            if user_id in latest_image_cache:
                filename, image_bytes = latest_image_cache[user_id]
                return Response(image_bytes, mimetype='image/jpeg')
        
        # 缓存中没有，从文件系统读取最新图片
        user_image_dir = os.path.join(IMAGE_SAVE_DIR, user_id)
        if not os.path.exists(user_image_dir):
            return jsonify({'code': 404, 'message': 'No images found'}), 404
        
        # 获取所有图片文件，按时间排序，取最新的
        image_files = glob.glob(os.path.join(user_image_dir, "*.jpg"))
        if not image_files:
            return jsonify({'code': 404, 'message': 'No images found'}), 404
        
        # 按修改时间排序，取最新的
        image_files.sort(key=os.path.getmtime, reverse=True)
        latest_file = image_files[0]
        filename = os.path.basename(latest_file)
        
        # 读取文件并返回
        with open(latest_file, 'rb') as f:
            image_bytes = f.read()
        
        # 更新缓存
        with cache_lock:
            latest_image_cache[user_id] = (filename, image_bytes)
        
        return Response(image_bytes, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/drone_images/<user_id>/<filename>', methods=['GET'])
def serve_image(user_id, filename):
    try:
        # 首先检查缓存
        cache_key = (user_id, filename)
        with cache_lock:
            if cache_key in image_cache:
                # 从缓存返回图片
                image_bytes = image_cache[cache_key]
                return Response(image_bytes, mimetype='image/jpeg')
        
        # 缓存中没有，从文件系统读取
        user_image_dir = os.path.join(IMAGE_SAVE_DIR, user_id)
        return send_from_directory(user_image_dir, filename)
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
