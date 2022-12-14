from asyncio.log import logger
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

app = Flask(__name__)
app.config.from_object('config')


# Create database connection object
db = SQLAlchemy(app)
#db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

logger = logging.getLogger("monlog")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)
formatter =logging.Formatter("%(levelname)-8s %(asctime)s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

from App import views, models


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return models.User.query.get(int(user_id))


@app.cli.command("init_db")
def init_db():
    models.init_db()

