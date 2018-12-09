"""Contains all the config for our smartmirror plugins and app."""

import os
import yaml
import json


class BaseConfig:
    """Base Config for our application."""

    with open("config.yml", "r") as stream:
        plugin_config = yaml.load(stream)

    with open("plugin_library.json", "r") as plugins:
        plugin_library = json.load(plugins)

    SECRET_KEY = plugin_config.get("secret_key", "123456")
    SM_VERSION = '1.0.0'
    PLUGIN_LIB = plugin_library


class ProductionConfig(BaseConfig):
    """Production config for the application."""

    ENV = 'production'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/smartmirror/data_files/main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """Testing config for the application."""

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ENV = 'THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION.'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/smartmirror/data_files/main.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
