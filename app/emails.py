from threading import Thread
from flask import current_app, render_template, redirect
from flask_mail import Message

from app import email


def send_email(to, **kwargs):
    app = current_app._get_current_object()
    msg = Message('邮箱验证',
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template('email_confirm.txt', **kwargs)  # 一个电子邮件要二个模板，一个用来存文本版本
    email.send(msg)
    return redirect('static/index.html')