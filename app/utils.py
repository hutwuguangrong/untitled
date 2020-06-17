from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # token的一个包

from flask import current_app


def generate_email_confirm_token(user, expiration=3600):  # 基于令牌的身份验证
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'email': user.email}).decode('utf-8')


def verify_email_confirm_token(token):  # 验证令牌
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return None
    return data['email']