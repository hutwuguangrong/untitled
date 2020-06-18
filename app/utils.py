from itertools import permutations
from string import ascii_letters, digits

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # token的一个包
import hashlib
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


def generate_password_hash_hash(password_hash):
    return hashlib.md5(password_hash.encode('UTF-8')).hexdigest()


def verify_password_hash_hash(email, password_hash_hash):
    pass


def decrypt_md5(md5_value):
    all_letters = ascii_letters + digits + '.,;'
    if len(md5_value)!=32:
        print('error')
        return
    md5_value=md5_value.lower()
    for k in range(5,10):
        for item in permutations(all_letters,k):
            item=''.join(item)
            if hashlib.md5(item.encode()).hexdigest()==md5_value:
                return item


