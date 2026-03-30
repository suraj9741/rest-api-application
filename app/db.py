from flask_sqlalchemy import SQLAlchemy
from app.config import settings

db = SQLAlchemy()

def init_db(app):
    # ✅ Only set DB if NOT already provided (important)
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)