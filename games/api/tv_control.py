"""
TV Control Game API endoints
"""

from flask import Flask, jsonify, request
from games.api import tv_api
from models import db


@tv_api.route('', methods=['GET'], strict_slashes=False)
def api():
    return jsonify({'status': 'OK'})


def get_tv_data():
    """ get data for tv control game """
    control_ref = db.collection(u'tv_control').document(u'data')
    doc = control_ref.get()
    print(doc.to_dict())
    return doc.to_dict()

@tv_api.route('/power', methods=['POST'])
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

@tv_api.route('/tv_status', methods=['GET'])
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
