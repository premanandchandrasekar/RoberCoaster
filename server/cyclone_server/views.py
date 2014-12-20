import re
from cyclone_server.db.postgres import PostgresDatabase
from twisted.internet import defer
from cyclone_server import utils
from cyclone_server.utils import BaseHandler
from cyclone_server.db.mixin import DatabaseMixin
from cyclone_server.api import SearchHandler
import goslate

class IndexHandler(BaseHandler, DatabaseMixin):
    is_index_handler = True
    
    def get(self):
        self.render("Index.html")
        
        
class SampleWebcamHandler(BaseHandler):

    def get(self):
        self.render("webcam.html")


class Scheme(BaseHandler, DatabaseMixin):
    @defer.inlineCallbacks
    def get(self, sid=None):
        if sid:
            jsonData = yield self.search_engine.searchv2(self.current_user, sid)
            print "1111111111111111"
            result = jsonData['hits']['hits'][0]['_source']
            self.render("update_scheme.html", sid=sid ,values=result)
        else:
            self.render("add_scheme.html")
