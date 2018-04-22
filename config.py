"""Contains all the config for our smartmirror plugins and app."""

import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
	"""Base Config for our application."""

	SECRET_KEY = '123456789' # TODO Change


class ProductionConfig(BaseConfig):
	"""Production config for the application."""
	DEBUG = False
	NJT = 'testconfigvalue'