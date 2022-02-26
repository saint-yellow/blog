from config import config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

boostrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
pagedown = PageDown()
login_manager = LoginManager()
# login_manager.login_view = 'auth.login'


def create_app() -> Flask:
    # Flask instance
    app = Flask(__name__)
    app.config.update(**config)

    # Flask extensions
    boostrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    pagedown.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .admin import admin as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
