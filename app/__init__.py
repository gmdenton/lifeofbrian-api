from flask import Flask
import logging

app = Flask(__name__, instance_relative_config=True)


def create_app():
    app.config.from_object('config')
    app.config.from_pyfile('config.py')


create_app()
logging.getLogger(__name__).addHandler(logging.NullHandler())