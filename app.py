from flask import (Flask, render_template,url_for, request,redirect,flash)
from flask_login import login_user, logout_user, login_required,LoginManager, UserMixin
from flask_caching import Cache
from datetime import datetime
from werkzeug.utils import secure_filename

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


from views import *

if __name__ == '__main__':
    app.run(debug=True)
