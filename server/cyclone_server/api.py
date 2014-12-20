import os
import goslate
import json
#from PIL import Image
#from pytesseract import image_to_string
from twisted.python import log
from StringIO import StringIO

import cyclone
from cyclone_server.db import mixin
from cyclone_server import utils 
from cyclone_server.utils import BaseHandler
from cyclone_server.db.mixin import DatabaseMixin
from cyclone_server import config
from twisted.internet import defer

gs = goslate.Goslate()

class APIBase(BaseHandler, DatabaseMixin):
    no_xsrf = True

    def get_config(self):
        path = config.config_file_path()
        settings = config.parse_config(path)
        return settings

    def prepare(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")

    def write_json(self, d):
        self.set_header("Content-Type", "application/json")
        return self.write(json.dumps(d, sort_keys=True, indent=4))

class UploadScheme(APIBase):

    @defer.inlineCallbacks
    def post(self):
        jsonData = json.loads(self.get_argument('jsonData'))
        to_update = jsonData.get('to_update_id',None)
        if to_update:
             jsonData = yield self.search_engine.addData(jsonData,to_update)
        else:
            jsonData = yield self.search_engine.addData(jsonData)
        
        print jsonData
        jsonData['success'] = True
        defer.returnValue(self.write_json(jsonData))
    
    
class SearchHandler(APIBase):

    @defer.inlineCallbacks
    def get(self):
        q = self.get_argument('q', None)
        limit = self.get_argument('limit', 100)
        skip = self.get_argument('skip', 0)
        if not q:
            msg = {'hits': [], 'success': False, 'code': 400, 'msg': 'Invalid search string'}
            defer.returnValue(self.write_json(msg))

        query = json.loads(q)
        q = query.get('term', '')
        terms = query.get("terms", [])

        lang = query.get("lang", "en")

        q = q[:100]  # Limit search entry to 100 chars
        q = q.replace('\\', '\\\\')              # escape slash to avoid json encoding error and server error
        jsonData = yield self.search_engine.searchv2(self.current_user, q, terms, limit, skip)
        # Removing `_id` fields from the result
        # as we dont want to expose integer ids

        if not 'code' in jsonData or jsonData['code'] == 500:
            log.msg('search engine did not return any data')

            msg = {'hits': [],
                    'success': False,
                    'code': 500,
                    'msg': 'Ah, seems the rogue monkeys are back at our servers!!! <br> Search Service is down. We are trying to get it back, sorry!'}

            defer.returnValue(self.write_json(msg))

        if lang != "en":
            new_hits = []
            for x in jsonData['hits']['hits']:
                x["_source"]["name"] = gs.translate(x["_source"]["name"], lang)
                x["_source"]["objectives"] = gs.translate(x["_source"]["objectives"], lang)
                x["_source"]["coverage"] = gs.translate(x["_source"]["coverage"], lang)
                new_hits.append(x)
            jsonData['hits']['hits'] = new_hits

        jsonData['success'] = True
        defer.returnValue(self.write_json(jsonData))

cam_counter = 0

class CamUploadHandler(APIBase):
    def post(self):
        #global cam_counter
        datafile = self.request.files['webcam'][0]
        #file_path = "uploads/" + str(cam_counter) + ".jpg"
        #cam_counter += 1
        #with open(file_path, 'wb') as f:
        #    f.write(datafile['body'])
        img_file = Image.open(StringIO(datafile['body'])).convert('L')
        img_file = img_file.point(lambda x: 0 if x<100 else 255, '1')
        text = image_to_string(img_file)
        #os.remove(file_path)
        pan_card = [x for x in text.split() if len(x) == 10]
        pan_card = pan_card[0] if len(pan_card) == 1 else None
        if pan_card and pan_card[:5].isalpha() and pan_card[5:9].isdigit() and pan_card[-1].isalpha():
            print 
            print "11111111111111111111111111111"
            print pan_card
            print "11111111111111111111111111111"
            print
        else:
            pan_card = "11"
        return self.write_json({'success': True, 'text': text, 'pan': pan_card})
