from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c39f53dab6fa151e766c5325943c6e59b4783dd3c909b47568de52b6957921e8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motors.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from app import routes