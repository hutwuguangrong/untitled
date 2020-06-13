import os
from flask import Flask

from .config import config
from .extentions import db, email, login_manager, api
from .models import User


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)  # flask的应用实例，所有的客户端请求都是这个实例处理
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprints(app)
    register_extensions(app)
    register_shell_context(app)

    return app


def register_blueprints(app):
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)


def register_extensions(app):
    db.init_app(app)
    email.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return None

    api.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor  # 要想进入shell时将对象自动导入列表中，必须用这个装饰器，注册一个shell上下文处理器
    def make_shell_context():
        return dict(db=db, User=User)

