from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# build relationship with DB
db = SQLAlchemy(app)
# binding app and DB for later usage
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import route, models
