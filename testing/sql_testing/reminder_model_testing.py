"""Unit testing for the reminder model."""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import sys

sys.path.append('../../')

from smartmirror.extensions import db


def create_app():
    """Main app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///reminder_test.db'
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    from test_view import test
    app.register_blueprint(test)

    return app

if __name__ == "__main__":
	app = create_app()
	app.run()
