from flask import Flask
from .extensions import bootstrap, cache
import yaml


def create_app():
	app = Flask(__name__)
	app.config.from_object('config.ProductionConfig')

	with open("config.yml", 'r') as stream:
		plugin_config = yaml.load(stream)
	app.config.update(plugin_config)
	app.config.update({'CACHE_TYPE': 'simple'})

	from views import blueprint
	app.register_blueprint(blueprint)

	if app.config.get('right_top_panel'):
		from views import right_top
		app.register_blueprint(right_top)

	if app.config.get('top_banner'):
		from views import top_banner_blueprint
		app.register_blueprint(top_banner_blueprint)

	bootstrap.init_app(app)
	cache.init_app(app, config=app.config)

	return app
