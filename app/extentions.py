from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_restplus import Api

db = SQLAlchemy()
email = Mail()
login_manager = LoginManager()
api = Api()