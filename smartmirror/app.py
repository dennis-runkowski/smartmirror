"""Main application factory."""
from flask import Flask
import logging
from .extensions import bootstrap, db
import yaml


def create_app():
    """Main app."""
    app = Flask(__name__)

    # Setup config and logging
    with open("config.yml", 'r') as stream:
        plugin_config = yaml.load(stream)

    if plugin_config.get("environment") == 'testing':
        app.config.from_object('config.TestingConfig')
        app.logger.setLevel(logging.DEBUG)
    else:
        app.config.from_object('config.ProductionConfig')
        app.logger.setLevel(logging.WARN)

    app.config.update(plugin_config)

    # Create main database before the first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    # Register the main blueprint
    from views import blueprint
    app.register_blueprint(blueprint)

    # Register the appropriate blueprints
    if app.config.get('top_banner'):
        from views import top_banner_blueprint
        app.register_blueprint(top_banner_blueprint)

    if app.config.get('right_top_panel'):
        from views import right_top_blueprint
        app.register_blueprint(right_top_blueprint)

    if app.config.get('right_bottom_panel'):
        from views import right_bottom_blueprint
        app.register_blueprint(right_bottom_blueprint)

    if app.config.get('left_panel'):
        from views import left_blueprint
        app.register_blueprint(left_blueprint)

    if app.config.get('bottom_banner'):
        from views import bottom_banner_blueprint
        app.register_blueprint(bottom_banner_blueprint)

        # Web UI to save reminders
        if app.config.get("bottom_banner").keys()[0] == 'reminders':
            from views import reminders_ui
            app.register_blueprint(reminders_ui)

    register_extensions(app)

    return app


def register_extensions(app):
    """Register flask extensions."""
    bootstrap.init_app(app)
    db.init_app(app)
