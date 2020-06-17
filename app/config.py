import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'gggjklsdjflsdjkf'

    MAIL_SUBJECT = 'Register'  # 邮件的主题
    MAIL_SERVER = 'smtp.qq.com'  # 邮件相关配置
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '419259833@qq.com'
    MAIL_PASSWORD = 'zcdphnwmtzuobhii'
    MAIL_SENDER = '419259833@qq.com'
    FLASK_MAIL_ADMIN = '419259833@qq.com'
    FLASK_ADMIN = '419259833@qq.com'

    JSON_AS_ASCII = False  # 使jsonify能返回中文

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 数据库配置

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
   SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TsetingCongig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost/test1mail'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost/test2mail'


config = {
    'development': DevelopmentConfig,
    'testing': TsetingCongig,
    'production': ProductionConfig
}