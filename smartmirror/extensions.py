from flask_bootstrap import Bootstrap
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

cache = Cache()
bootstrap = Bootstrap()
db = SQLAlchemy()
