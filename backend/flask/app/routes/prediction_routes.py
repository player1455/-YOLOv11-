from flask import Blueprint, request, jsonify, Response
import logging

from app.services.prediction_service import PredictionService

prediction_bp = Blueprint('prediction', __name__)

def init_prediction_service(service: PredictionService):
    prediction_bp.service = service

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'code': 400, 'message': 'No data provided'}), 400
        
        user_id = data.get('userId', 'default')
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'code': 400, 'message': 'Image data is required'}), 400
        
        result = prediction_bp.service.predict(user_id, image_data)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result
        })
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@prediction_bp.route('/latest_image/<user_id>', methods=['GET'])
def get_latest_image(user_id):
    try:
        filename, image_bytes = prediction_bp.service.get_latest_image(user_id)
        return Response(image_bytes, mimetype='image/jpeg')
    except FileNotFoundError:
        return jsonify({'code': 404, 'message': 'No images found'}), 404
    except Exception as e:
        logging.error(f"Get latest image error: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@prediction_bp.route('/drone_images/<user_id>/<filename>', methods=['GET'])
def get_image(user_id, filename):
    try:
        image_bytes = prediction_bp.service.get_image(user_id, filename)
        return Response(image_bytes, mimetype='image/jpeg')
    except FileNotFoundError:
        return jsonify({'code': 404, 'message': 'Image not found'}), 404
    except Exception as e:
        logging.error(f"Get image error: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@prediction_bp.route('/get_image_history', methods=['GET'])
def get_image_history():
    try:
        user_id = request.args.get('userId', 'default')
        images = prediction_bp.service.get_image_history(user_id)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'images': images
            }
        })
    except Exception as e:
        logging.error(f"Get image history error: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500

@prediction_bp.route('/delete_image', methods=['POST'])
def delete_image():
    try:
        data = request.get_json()
        user_id = data.get('userId', 'default')
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'code': 400, 'message': 'Filename is required'}), 400
        
        success = prediction_bp.service.delete_image(user_id, filename)
        
        if success:
            return jsonify({'code': 200, 'message': 'success'})
        else:
            return jsonify({'code': 404, 'message': 'Image not found'}), 404
    except Exception as e:
        logging.error(f"Delete image error: {e}")
        return jsonify({'code': 500, 'message': str(e)}), 500
