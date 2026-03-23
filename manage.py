from app import create_app
from app.db import db

app = create_app()

# Required for Flask-Migrate
@app.shell_context_processor
def make_shell_context():
    return {"db": db}