from flask import Blueprint, redirect, url_for, current_app

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return redirect(url_for('file.index'))

# 图标
@bp.route('/favicon.ico') 
def get_favicon(): 
    return current_app.send_static_file('favicon.ico')