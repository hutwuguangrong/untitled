from flask import g, request, jsonify, abort, redirect, url_for, flash, render_template, make_response
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Resource

from app import api, db
from . import auth_bp
from ..models import User

auth = HTTPBasicAuth()  # 这里面没有参数


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth_bp.route('/api/auth/register')
def register():
    return render_template('login.html')


@api.route('/api/auth/register')
class register(Resource):
    def post(self):
        """
        用户注册
        :receive:
        email:邮箱
        password：密码
        name：用户名
        :return:
        """
        email = request.values.get('email')  # 为什么要用values,不用json
        password = request.values.get('password')
        name = request.values.get('name')
        user = User(email=email, password=password, name=name)
        if User.query.filter_by(email=email).first() is not None:
            flash('该邮箱已经注册！')
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash('注册成功！')
        return redirect(url_for('login'))


@api.route('/token')
class get_token(Resource):
    @auth.login_required()
    def post(self):
        """
        token登录，产生token的功能
        :receive:
        None
        :return:
        token：产生的token
        time：token有效的时间
        message：包含一下显示的信息
        """
        if g.current_user.is_anonymous or g.token_used:
            abort(403)
        return jsonify({
            'token': g.current_user.generate_auth_token(),
            'message': 'ok'
        })


@auth_bp.route('/api/auth/login')
def login():
    return render_template('login.html')


@api.route('/api/auth/login')
class login(Resource):
    def post(self):
        """
        登录
        :receive:
        email：邮箱
        password：密码
        :return:
        密码正确跳转到其他页面
        密码错误提示密码错误
        """
        email = request.values.get('email')
        password = request.values.get('password')
        user = User.query.filter_by(email=email).first()
        if user is None or user.verify_password(password) is False:
            flash('你的邮箱或者密码错误！')
            return redirect(url_for('login'))
        return redirect(url_for('index'))


