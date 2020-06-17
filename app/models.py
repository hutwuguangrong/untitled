from datetime import datetime


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    name = db.Column(db.String(64), index=True)
    confirmed = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_user = {
            'name': self.name,
            'email': self.email
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<email %r>' % self.email


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qrcode_filename = db.Column(db.String(20))
    name = db.Column(db.Text())
    current_agent = db.Column(db.Integer)
    sold = db.Column(db.Boolean, default=False)
    sold_time = db.Column(db.DateTime())
    sold_location = db.Column(db.Text)
    production_date = db.Column(db.DateTime(), default=datetime.utcnow)
    main_ingredient = db.Column(db.Text())


class superior_ubordinate(db.Model):
    superior_id = db.Column(db.Integer, db.ForeignKey('agent.id'), primary_key=True)
    ubordinate_id = db.Column(db.Integer, db.ForeignKey('agent.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    superior = db.relationship('superior_ubordinate',
                               foreign_keys=[superior_ubordinate.ubordinate_id],
                               backref=db.backref('ubordinate', lazy='joined'),
                               lazy='dynamic')

    ubordinate = db.relationship('superior_ubordinate',
                                foreign_keys=[superior_ubordinate.superior_id],
                                backref=db.backref('superior', lazy='joined'),
                                 lazy='dynamic')








