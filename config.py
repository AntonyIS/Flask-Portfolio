import os
DEBUG = False
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ "/Portfolio/static/images"
UPLOAD_FOLDER = BASE_DIR
PASSWORD = 'pass1234'
EMAIL = 'antonyshikubu@gmail.com'

