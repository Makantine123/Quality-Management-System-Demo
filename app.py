#!/usr/bin/env python3
"""Flask App"""
import logging
from flask_login import LoginManager
from jinja2 import FileSystemLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template
from flask_cors import CORS
from models.base_model import BaseModel
from models.users import Users
from routes.auth import auth_views, github_blueprint, google_blueprint
from routes.dashboard import dash_views
from routes.inv import inv_views
from routes.tsk import tsk_views
from config import Config

Session = None


def create_app():
    """ Create and Configure flask App """
    app = Flask(__name__)
    app.config.from_object(Config)

    initialize_extentions(app)
    setup_database(app)
    register_error_handlers(app)
    register_all_blueprints(app)
    CORS(app)
    return app


def register_all_blueprints(app):
    """ Register Blueprints """
    app.register_blueprint(auth_views)
    app.register_blueprint(dash_views)
    app.register_blueprint(inv_views)
    app.register_blueprint(tsk_views)
    app.register_blueprint(github_blueprint)
    app.register_blueprint(google_blueprint)


def initialize_extentions(app):
    """ Initialize Flask extentions """
    app.jinja_loader = FileSystemLoader('templates')

    def format_date(value, format='%Y-%m-%d'):
        if value is not None:
            return value.strftime(format)
        return ''

    app.jinja_env.filters['format_date'] = format_date
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'home'
    login_manager.login_message_category = 'login_warning'

    @login_manager.user_loader
    def load_user(user_id):
        """ User Loader """
        db = Session()
        return db.query(Users).filter_by(id=user_id).first()


def setup_database(app):
    """ Set up the database """
    global Session
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = scoped_session(sessionmaker(bind=engine))
    app.session = Session
    print('Session set up: ', app.session)
    BaseModel.metadata.create_all(engine)


def register_error_handlers(app):
    """ Register Error handlers """

    @app.errorhandler(400)
    def bad_request_error(error):
        """ Bad Request Error handler """
        return render_template('400.html'), 400

    @app.errorhandler(404)
    def not_found_error(error):
        """ Not found erro """
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """ Internal Server Error """
        return render_template('500.html'), 500


app = create_app()


@app.route('/')
def home():
    """ Landing Page Route """
    return render_template('index.html')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
