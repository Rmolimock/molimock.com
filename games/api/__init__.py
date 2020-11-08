from flask import Blueprint

tv_api = Blueprint("tv_api", __name__, url_prefix="/games/tv/api")

from games.api.tv_control import *

 