"""
################################
Flask Application Initialization
################################

This `__init__.py` file sets up the Flask application.

..todo::
    Comment this flask app initialization.

"""

# Basic package imports.
import os

# Basic flask specific imports.
from flask import Flask, render_template

# Flask extension imports.
from flas_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Instantiate the extensions.
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
    Create the flask application.
    """

    # Instantiate the application.
    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static',
    )

    # Set up the configuration.
    app_settings = os.getenv(
        'APP_SETTINGS',
        'project.server.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)

    # Set up the extensions.
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints.
    from project.server.user.views import user_blueprint
    from project.server.main.views import main_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)

    # Set up the flask login extension.
    from project.server.models import User
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

        # What is this? Does this code ever run?
        return app

    # Create error handlers.
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500

    return app
