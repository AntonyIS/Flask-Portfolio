
import os
DEBUG = False
SECRET_KEY = os.urandom(24)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.sqlite'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Portfolio'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/Portfolio/static/images"

PASSWORD = 'pass1234'
EMAIL = 'antonyshikubu@gmail.com'

