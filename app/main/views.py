from flask import jsonify, render_template
from flask_restplus import Resource

from app import api
from app.main import main_bp


@main_bp.route('/index')
def index():
        return render_template('login.html')