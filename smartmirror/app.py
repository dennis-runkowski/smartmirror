from flask import Flask
import os


def create_app():
	app = Flask(__name__)
	app.config.from_object('config.ProductionConfig')
	# print app.config.from_object('config').get('NJT')
	print app.config["NJT"]

	from views import blueprint
	app.register_blueprint(blueprint)

	return app