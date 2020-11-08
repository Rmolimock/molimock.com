"""
Tv Control Game
"""
from games import tv
from flask import render_template, jsonify




@tv.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """ TV Control Game uses a single page """
    return render_template('games/tv_control.html')