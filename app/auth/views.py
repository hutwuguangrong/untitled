
from flask import request, jsonify, make_response
from flask_restplus import Resource
import re

from app import api, db
from ..emails import send_email
from ..models import User
from ..utils import generate_email_confirm_token, verify_email_confirm_token


@api.route('/api/auth/register')
class register(Resource):
    def post(self):
        """
        注册
        :请求参数:
            token string
            email string  用户注册的邮箱
            password string 用户注册的密码
            name string 用户的用户名

        :返回字段：
            message string 需要alert的信息

        """
        email = request.values.get('email')  # 为什么要用values,不用json
        password = request.values.get('password')
        name = request.values.get('name')
        user = User(email=email, password=password, name=name)
        if email == '':
            return make_response(jsonify({'message': '邮箱不能为空！'}), 400)
        if User.query.filter_by(email=email).first() is not None:
            return make_response(jsonify({'message': '该邮箱已经注册！'}), 400)

        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is None:
            return make_response(jsonify({'message': '邮箱格式错误！'}), 400)

        if password == '':
            return make_response(jsonify({'message': '密码不能为空！'}), 400)

        db.session.add(user)
        db.session.commit()
        token = generate_email_confirm_token(user)
        send_email(user.email, user=user, token=token)
        return make_response(jsonify(({'message': '请到您的邮箱完成验证！'})), 200)


@api.route('/api/auth/login')
class login(Resource):
    def post(self):
        """
        登录
        :亲求参数:
        email string 用户的邮箱
        password string 用户的密码
        :返回字段:
        message string 需要alert的内容

        """
        email = request.values.get('email')
        password = request.values.get('password')
        user = User.query.filter_by(email=email).first()
        if user is None or user.verify_password(password) is False:
            return make_response(jsonify({'message': '您的邮箱或者密码错误！'}), 400)
        if not user.confirmed:
            return make_response(jsonify(({'message': '您还没有验证邮箱，请验证邮箱再来登录！'})), 400)
        res = make_response(jsonify({'message': '登录成功！'}))
        res.status_code = 200
        res.set_cookie(key='token',  value='', expires=36000)
        res.set_cookie(key='email', value=email, expires=36000)
        return res


@api.route('/api/auth/logout')
class logout(Resource):
    def get(self):
        """
        退出登录
        :请求参数：
        无
        :返回字段:
        message
        """
        res = make_response(jsonify({'message': '退出登录成功！'}), 200)
        res.set_cookie(key='token', value='', expires=0)
        res.set_cookie(key='email', value='', expires=0)
        return res


@api.route('/api/auth/email_confirm/<token>')
class email_confirm(Resource):
    def get(self, token):
        """
        注册时，邮箱验证
        :请求参数:
        :param token:
        :返回字段:
        message
        """
        email = verify_email_confirm_token(token)
        if email == '':
            return make_response(jsonify({'message': '该链接已经无效！'}), 400)
        user = User.query.filter_by(email=email).first()
        if user.confirmed:
            return make_response(jsonify({'message': '你已经验证了您的邮箱，不需要重复确认！'}), 400)
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        res = make_response(jsonify({'message': '邮箱验证成功！'}), 200)
        return res
