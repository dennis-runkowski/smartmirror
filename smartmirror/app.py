from flask import Flask
from .extensions import bootstrap, cache, db
import yaml


def create_app():
	app = Flask(__name__)
	app.config.from_object('config.ProductionConfig')

	with open("config.yml", 'r') as stream:
		plugin_config = yaml.load(stream)
	app.config.update(plugin_config)
	app.config.update({'CACHE_TYPE': 'simple'})
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_files/main.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	@app.before_first_request
	def create_tables():
		db.create_all()

	from views import blueprint
	app.register_blueprint(blueprint)

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

	bootstrap.init_app(app)
	db.init_app(app)
	cache.init_app(app, config=app.config)

	return app
