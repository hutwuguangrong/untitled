from flask import jsonify
from flask_restplus import Resource

from app import api


@api.route('/index')
class index(Resource):
    def get(self):
        return jsonify({
            'message': '登录成功！'
        })
