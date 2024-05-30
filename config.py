"""Config Module"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'server', 'database.db')


class Config:
    """App Config Class"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-key-my-key')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = '427602012949-agtvtuu6l8gfs2c3h0qo900imb2k4evt.apps.googleusercontent.com'
    GOOGLE_SECRET = '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'
    GITHUB_CLIENT_ID = 'Ov23liELB2X3erDOHOn7'
    GITHUB_SECRET = 'db753dcfd2dd9ba5ec766271366becadddb4f60a'
    UPLOAD_FOLDER = 'server/files/'
