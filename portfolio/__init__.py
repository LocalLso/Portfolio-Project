from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SECRET_KEY'] = '626f47136c41741b5d887d811e4d718a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['MAX_CONTENT_LENGTH'] =100 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['.pdf', '.docx']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.app_context().push()

from portfolio import routes
