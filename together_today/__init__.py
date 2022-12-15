#EDIT blueprints

import os
from flask import Flask
#from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate, upgrade
from flask_login import LoginManager


def create_app(config="together_today.config.Config"):
    app = Flask(__name__, static_folder="dist", static_url_path="/static")

    with app.app_context():
        app.config.from_object(config)

    

        # pylint: disable=import-outside-toplevel
        from together_today.models import db

        db.init_app(app)
        Migrate(app, db)
        upgrade()

        login_manager = LoginManager()
        login_manager.login_view = "auth.login"
        login_manager.init_app(app)

        from .models import User

        @login_manager.user_loader
        def load_user(user_id: int):
            return User.query.get(int(user_id))

        # pylint: disable=import-outside-toplevel
        from together_today.views import general

        app.register_blueprint(general)
       

    return app
