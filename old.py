# [START gae_python38_app]
from flask import Flask, request, render_template, jsonify
# from models import db
from games.tv_control import auth


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.register_blueprint(auth.bp)

'''
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Nice try Joe. No peaking!'

@app.route('/control', methods=['GET'])
def control_view():
    return render_template('control.html')


def get_tv_data():
    """ get data for tv control game """
    control_ref = db.collection(u'tv_control').document(u'data')
    doc = control_ref.get()
    print(doc.to_dict())
    return doc.to_dict()

@app.route('/power', methods=['POST'])
def power():
    """ toggle power on tv, potentially changing who has control """
    from datetime import datetime, timedelta
    # get action and viewer from clientr
    viewer = request.json['viewer']
    action = request.json['action']

    #get data from database
    data = get_tv_data()
    data_ref = db.collection(u'tv_control').document(u'data')
    # is tv on or off
    tv_status = action
    data_ref.set({u'tv_status': tv_status}, merge=True)
    # who has control, if anyone
    controller = data['controller']
    print('controller is', controller, 'and tv is being turned', action, 'by', viewer)

    # get current time
    now = datetime.now()
    # has control expired
    last_str = data['last_watched']
    # deserialize last watched date
    last_watched = datetime.strptime(last_str, "%d-%b-%Y (%H:%M:%S.%f)")
    # if control has expired
    if now > last_watched + timedelta(hours=1):
        controller = 'No one'
        # save change to controller
        data_ref.set({u'last_watched': now.strftime("%d-%b-%Y (%H:%M:%S.%f)")}, merge=True)
        data_ref.set({u'controller': 'No one'}, merge=True)
    if controller == viewer:
        # update last_watched time
        data_ref.set({u'last_watched': now.strftime("%d-%b-%Y (%H:%M:%S.%f)")}, merge=True)
        if action == 'off':
            # give up control
            controller = 'No one'
            data_ref.set({u'controller': 'No one'}, merge=True)
    if controller == 'No one' and action == 'on':
        # you gain control
        controller = viewer
        data_ref.set({u'controller': viewer}, merge=True)
        data_ref.set({u'last_watched': now.strftime("%d-%b-%Y (%H:%M:%S.%f)")}, merge=True)

    return controller

@app.route('/tv', methods=['GET'])
def tv():
    """ check if tv is on and who has control """
    from datetime import datetime, timedelta
    data = get_tv_data()
    data_ref = db.collection(u'tv_control').document(u'data')

    # who has control, if anyone
    controller = data['controller']
    print('controller is', controller)

    # get current time
    now = datetime.now()
    # has control expired
    last_str = data['last_watched']
    # deserialize last watched date
    last_watched = datetime.strptime(last_str, "%d-%b-%Y (%H:%M:%S.%f)")
    # if control has expired
    if now > last_watched + timedelta(hours=1):
        controller = 'No one'
        # save change to controller
        data_ref.set({u'controller': 'No one'}, merge=True)
        data_ref.set({u'last_watched': now.strftime("%d-%b-%Y (%H:%M:%S.%f)")}, merge=True)

    return jsonify({'controller': controller, 'tv_status': data['tv_status']})




@app.route('/data', methods=['POST', 'GET'])
def data():
    """Test adding data to the firestore db"""
    name = request.form.get('name')
    if not name:
        name = request.json['name']
    doc_ref = db.collection(u'users').document(u'{}'.format(name))
    doc_ref.set({
        u'first': u'{}'.format(name.split(' ')[0]),
        u'last': u'{}'.format(name.split(' ')[1])
    })
    return 'Thanks!'

"""

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>

            function sendAndRecieve(data=null, fill=null) {
                
                $.ajax({
                    type: 'POST',
                    url: '/data',

                    data: JSON.stringify(data) || JSON.stringify({'name':'jklads yajyyy'}),
                    contentType: 'application/json;charset=UTF-8',
                    success: function(data) {
                        $(fill).text(data);
                    },
                    error: function(data) {                        alert(data);
                        alert(data);
                    }
                });

            };
        </script>

"""



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python38_app]
'''