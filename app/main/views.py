from flask import make_response, jsonify, request
from flask_restplus import Resource

from app import api
from app.utils import verify_email_confirm_token


@api.route('/index')
class index(Resource):
        def get(self):
                token = request.cookies.get('token', 'default1')
                email = request.cookies.get('email', 'default2')
                if email != verify_email_confirm_token(token):
                        return make_response(jsonify({'message': '请登录后再来请求该接口！'}), 401)
                return make_response(jsonify({'message': '成功！'}), 200)
