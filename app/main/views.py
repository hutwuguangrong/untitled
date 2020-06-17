from flask import jsonify, render_template, redirect
from app.main import main_bp


@main_bp.route('/index')
def index():
        return jsonify({'message': '112'}), 200