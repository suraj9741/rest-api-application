from flask import Flask
from app.routes import student_bp
from app.db import init_db, db
from flask_migrate import Migrate
import logging

migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.json.sort_keys = False

    logging.basicConfig(level=logging.INFO)

    if test_config:
        app.config.update(test_config)

    init_db(app)

    migrate.init_app(app, db)

    # register blueprint
    app.register_blueprint(student_bp)

    return app