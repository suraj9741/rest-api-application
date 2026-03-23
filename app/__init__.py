from flask import Flask
from app.routes import student_bp
import logging

def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False

    # logging
    logging.basicConfig(level=logging.INFO)

    # register blueprint
    app.register_blueprint(student_bp)

    return app