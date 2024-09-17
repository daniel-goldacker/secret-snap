import os
from flask import request, jsonify, send_file
from flask_restful import Resource
from utils import encode_message_in_image, decode_message_from_image

class EncodeMessage(Resource):
    def post(self):
        """Encode a secret message into an image."""
        if 'file' not in request.files or 'message' not in request.form:
            return {"error": "File or message not provided"}, 400

        file = request.files['file']
        message = request.form['message']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        output_image_name = 'encoded_image.png'
        instance_folder = os.path.join(os.path.dirname(__file__), 'instance')

        try:
            file.save('temp_image.png')
            output_image_path = encode_message_in_image('temp_image.png', message, output_image_name, instance_folder)
        except Exception as e:
            return {"error": str(e)}, 400
        finally:
            os.remove('temp_image.png')  # Clean up

        return send_file(output_image_path, mimetype='image/png')

class DecodeMessage(Resource):
    def post(self):
        """Decode a secret message from an image."""
        if 'file' not in request.files:
            return {"error": "File not provided"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        try:
            file.save('temp_image.png')
            message = decode_message_from_image('temp_image.png')
        except Exception as e:
            return {"error": str(e)}, 400
        finally:
            os.remove('temp_image.png')  # Clean up

        return jsonify({"message": message})
