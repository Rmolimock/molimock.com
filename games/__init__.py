from flask import Blueprint

tv = Blueprint("tv", __name__, url_prefix="/games/tv")

from games.tv_control import *

 