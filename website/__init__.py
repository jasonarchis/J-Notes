from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path 


DB_NAME = "database.db"
db = SQLAlchemy()

# Initialise app, database, and LoginManager
def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jjoanshucyh11389bhb723b9:11129^f'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from.views import views
    from.auth import auth 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
