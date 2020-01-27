from flask import (Flask, render_template,url_for, request,redirect,flash)
from flask_login import login_user, logout_user, login_required,LoginManager, UserMixin
from flask_caching import Cache
from datetime import datetime

import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Portfolio/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(BASE_DIR,'static/image')


from views import *

if __name__ == '__main__':
    app.run(debug=True)
