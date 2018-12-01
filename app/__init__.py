from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

#build relationship with DB
db = SQLAlchemy(app)
#binding app and DB for later usage
migrate = Migrate(app, db)

from app import route, models
