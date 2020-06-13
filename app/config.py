import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'gggjklsdjflsdjkf'

    JSON_AS_ASCII = False  # jsonify返回中文

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