import os
from flask import Flask, request, jsonify, send_file
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from config import Config
from resources import EncodeMessage, DecodeMessage

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

app.register_blueprint(swaggerui_blueprint, url_prefix=app.config['SWAGGER_URL'])

# Register resources with Flask-RESTful
api.add_resource(EncodeMessage, '/encode')
api.add_resource(DecodeMessage, '/decode')

if __name__ == '__main__':
    app.run(debug=False)
