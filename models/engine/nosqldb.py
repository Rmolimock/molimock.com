from google.cloud import firestore


# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

class TvControl():
    """ data for tv control page """
    def __init__(self):
        from datetime import datetime
        self.controller = 'No one'
        self.tv_status = 'off'
        self.last_watched = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    def to_dict(self):
        d = {}
        d['controller'] = self.controller
        d['tv_status'] = self.tv_status
        d['last_watched'] = self.last_watched
        return d



tv_control_ref = db.collection(u'tv_control')
tv_control_ref.document(u'data').set(TvControl().to_dict())
