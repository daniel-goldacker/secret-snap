import os
from flask import Flask, request, jsonify, send_file
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_restful import Resource
from config import Config
from utils import encode_message_in_image, decode_message_from_image


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

# Swagger configuration
swaggerui_blueprint = get_swaggerui_blueprint(
    app.config['SWAGGER_URL'],
    app.config['API_URL'],
    config={'app_name': "secret-snap"}
)

file_directory = app.instance_path
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

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

        try:
            file.save('temp_image.png')
            output_image_path = encode_message_in_image('temp_image.png', message, output_image_name, file_directory)
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


app.register_blueprint(swaggerui_blueprint, url_prefix=app.config['SWAGGER_URL'])

# Register resources with Flask-RESTful
api.add_resource(EncodeMessage, '/encode')
api.add_resource(DecodeMessage, '/decode')

if __name__ == '__main__':
    app.run(debug=False)
