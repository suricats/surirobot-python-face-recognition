from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from management.mod_api.api import mod_api
app.register_blueprint(mod_api)

db.create_all()
