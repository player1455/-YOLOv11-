from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import base64
from ultralytics import YOLO
import io

app = Flask(__name__)
CORS(app)

model = YOLO('../../weights/best.pt')

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

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'code': 400, 'message': 'No data provided'}), 400
        
        user_id = data.get('userId')
        image = data.get('image')
        token = data.get('token')
        
        if not image:
            return jsonify({'code': 400, 'message': 'Image data is required'}), 400
        
        image_pil = base64_to_image(image)
        img_np = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        
        results = model.predict(source=img_np, imgsz=640, conf=0.25, iou=0.45, save=False)
        
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
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'boxes': boxes,
                'image': result_image_base64
            }
        })
        
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
