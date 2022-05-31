from flask import Flask, app
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

from config.settings import *
from api.routes import create_routes


def get_flask_app(config: dict = None, *args, **kwargs) -> app.Flask:
    """
    Initializes Flask app with given configuration.
    :param config: Optional configuration dictionary
    :return: app.Flask
    """
    # init flask
    flask_app = Flask(__name__)

    # configure app
    if config is not None:
        flask_app.config.update(config)

    flask_app.config.update(kwargs)

    # init mongo
    flask_app.config["MONGODB_SETTINGS"] = {
        'db': 'sloovi_db', 'host': MONGODB_URI}

    # load config variables for jwt from settings.py
    flask_app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    flask_app.config['JWT_COOKIE_SECURE'] = JWT_COOKIE_SECURE
    flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    flask_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES

    # init api and routes
    create_routes(Api(app=flask_app))

    # init mongoengine
    MongoEngine(app=flask_app)

    # init jwt manager
    JWTManager(app=flask_app)

    return flask_app


if __name__ == '__main__' and DEBUG:
    # Main entry point when run in stand-alone mode.
    app = get_flask_app()
    app.run(debug=DEBUG)
