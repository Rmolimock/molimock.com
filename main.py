from flask import Flask
from games import tv
from games.api import tv_api

app = Flask(__name__)
app.register_blueprint(tv)
app.register_blueprint(tv_api)


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """ molimock.com landing page """
    return 'under development'



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True) 