from flask import g, request, jsonify, abort
from flask_httpauth import HTTPBasicAuth
from flask_restplus import Resource


from app import api, db
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


@api.route('/api/auth/register')
class register(Resource):
    def post(self):
        """
        用户注册界面的api
        :你要给我的参数:
        email:邮箱
        password：密码
        name：用户名

        :我给你的参数（return）:
        message：包含有没有注册成功的信息
        """
        email = request.values.get('email')  # 为什么要用values,不用json
        password = request.values.get('password')
        name = request.values.get('name')
        user = User(email=email, password=password, name=name)
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({
                'message': '该邮箱已经注册!'
            })
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': '注册成功!'
        })


@api.route('/token')
class get_token(Resource):
    @auth.login_required()
    def post(self):
        """
        token登录，产生token的功能
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


