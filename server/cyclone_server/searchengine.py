from twisted.python import log
from twisted.internet import defer
import json
import sys
import traceback
from cyclone_server import httpclient
import lxml.html
from cyclone_server import consts
import calendar
import datetime
from HTMLParser import HTMLParser
from datetime import date, timedelta

import random

DISQUERY_NOTE_TYPE_NODE = 0
DISQUERY_NOTE_TYPE_LINK = 1

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def handle_starttag(self, tag, attrs):
        if tag == 'em':
            self.fed.append("<em>")

    def handle_endtag(self, tag):
        if tag == 'em':
            self.fed.append("</em>")

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def timestamp(crdate):
    return calendar.timegm(crdate.timetuple()) * 1000


class SearchEngine(object):
    def __init__(self, conf):
        self.config = conf

    @defer.inlineCallbacks
    def post_data(self, data, url, dbase=None):
        log.msg('search index post_data')
        index_url = 'http://%s:%s/%s/%s' % (
                 self.config.host, self.config.port,
                 self.config.index, url)

        try:
            log.msg('Indexing data Url:%s' % (index_url,))
            data = json.dumps(data)
            yield httpclient.fetch(index_url, method='POST', postdata=data)
            defer.returnValue(True)

        except Exception:
            log.msg('Error indexing data url: %s - %s : %s' % (
                index_url, sys.exc_info()[0], traceback.format_exc()))
            if dbase:
                dbase.add_to_index_queue(data, url, False)
            defer.returnValue(False)

    @defer.inlineCallbacks
    def post_feedsubscription(self, data, url, dbase=None):
        log.msg('search index post_feeddata')
        index_url = 'http://%s:%s/%s/%s' % (self.config.feed_host,
                                            self.config.feed_port,
                                            self.config.subscription_index,
                                            url)

        try:
            log.msg('Indexing feed subscription data Url:%s' % (index_url,))
            data = json.dumps(data)
            yield httpclient.fetch(index_url, method='POST', postdata=data)
            defer.returnValue(True)

        except Exception:
            log.msg('Error indexing feed subscription data url: %s - %s : %s' % (
                index_url, sys.exc_info()[0], traceback.format_exc()))
            #TODO: add to different queue
            #if dbase:
                #dbase.add_to_index_queue(data, url, False)
            defer.returnValue(False)

    @defer.inlineCallbacks
    def check_status(self):
        index_url = 'http://%s:%s' % (self.config.host, self.config.port)

        try:
            res = yield httpclient.fetch(index_url, method='GET')
            jsondata = json.loads(res.body)
            if jsondata['status'] == 200:
                defer.returnValue(True)
            else:
                defer.returnValue(False)

        except Exception:
            log.msg('Error reaching ES server - %s : %s' % (
                sys.exc_info()[0], traceback.format_exc()))
            defer.returnValue(False)

    @defer.inlineCallbacks
    def delete_data(self, data, url, dbase=None):
        index_url = 'http://%s:%s/%s/%s' % (
                 self.config.host, self.config.port,
                 self.config.index, url)

        try:
            log.msg('Deleting data %s - Url:%s' % (data, index_url))
            data = json.dumps(data)
            yield httpclient.fetch(index_url, method='DELETE', postdata=data)
            defer.returnValue(True)

        except Exception:
            log.msg('Error deleting data - %s : %s' % (
                sys.exc_info()[0], traceback.format_exc()))
            if dbase:
                dbase.add_to_index_queue(data, url, True)
            defer.returnValue(False)

    def index_document(self, document, document_version, filename, content, dbase):
        if isinstance(document_version, objects.DocumentVersion):
            doc_ver_id = document_version._id
        else:
            doc_ver_id = document_version.id

        if document.doc_type == 'html':
            #content = unicode(content, errors='ignore')
            #content = html2text.html2text(content)

            #Make sure we have only text (remove all html tags)
            try:
                t = lxml.html.fromstring(content)
                content = t.text_content()
            except Exception:
                log.msg('Error converting html to text. Using original html content for indexing')

        ind = {
            "did": doc_ver_id,
            "title": document.title,
            "dtype": document.doc_type,
            "fname": filename,
            "content": content,
            "ver": document_version.version,
            "uid": document_version.uploaded_by,
            "pid": document.project_id,
            #"file": None,
            "crdate": document_version.uploaded_on.strftime(consts.YYYMMDD_DATE_FORMAT),
            "guid": document_version.guid,
            }

        index_url = '%s/%s?parent=%s&timestamp=%s' % (
                self.config.document_type, doc_ver_id,
                document.project_id,
                timestamp(document_version.uploaded_on))
        self.post_data(ind, index_url, dbase)

    def index_documentmeta(self, document, document_version, entities, keywords, dbase):
        if isinstance(document_version, objects.DocumentVersion):
            doc_ver_id = document_version._id
        else:
            doc_ver_id = document_version.id

        tagl = None
        tagp = None
        tago = None
        tagkw = None

        if entities:
            try:
                tagl = entities.get('LOCATION', None)
                tagp = entities.get('PERSON', None)
                tago = entities.get('ORGANIZATION', None)
            except Exception:
                log.msg('error loading entities - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))

        if keywords:
            tagkw = keywords.get('KEYWORD', None)

        ind = {
            "did": doc_ver_id,
            "doctitle": document.title,
            "dtype": document.doc_type,
            "ver": document_version.version,
            "uid": document_version.uploaded_by,
            "pid": document.project_id,
            "guid": document_version.guid,
            "tagl": tagl,
            "tagp": tagp,
            "tago": tago,
            "tagkw": tagkw,
        }

        index_url = '%s/%s?parent=%s&timestamp=%s' % (
                                self.config.document_meta_type,
                                doc_ver_id,
                                document.project_id,
                                timestamp(document_version.uploaded_on))

        return self.post_data(ind, index_url, dbase)

    def remove_document(self, project_id, document_version, dbase):

        if isinstance(document_version, objects.DocumentVersion):
            doc_ver_id = document_version._id
        else:
            doc_ver_id = document_version.id

        pid = project_id

        #print 'deleting document meta from index'
        #4. delete doc meta
        url = '%s/%s?routing=%s' % (self.config.document_meta_type, doc_ver_id, pid)
        self.delete_data('', url, dbase)

        #print 'deleting document  from index'
        #5. delete doc
        url = '%s/%s?routing=%s' % (self.config.document_type, doc_ver_id, pid)
        self.delete_data('', url, dbase)

    def index_project(self, project, dbase):
        ind = {
                "title": project.project_name,
                "uid": project.owner_id,
                "crdate": project.created_on.strftime(consts.YYYMMDD_DATE_FORMAT),
                "guid": project.guid,
                "pid": project._id,
            }
        index_url = '%s/%s?timestamp=%s' % (
                self.config.project_type, project._id,
                timestamp(project.created_on))
        self.post_data(ind, index_url, dbase)

        #add project owner to prj access list
        self.index_userprojectaccesslist(project.owner_id, project._id, dbase)

    def remove_project(self, project, dbase):

        #print 'Remove project from index...'

        pid = project._id

        #keep both the query data strings handy
        qparent = {"term": {"_parent": pid}}
        qpid = {"term": {"pid": pid}}

        #print 'Remove doc meta'
        #3.4 delete metadata for all documents of the project
        url = '%s/_query?routing=%s' % (self.config.document_meta_type, pid)
        self.delete_data(qpid, url, dbase)

        #print 'Remove docs'
        #3.5 delete all documents of the project
        url = '%s/_query?routing=%s' % (self.config.document_type, pid)
        self.delete_data(qpid, url, dbase)

        #print 'Remove prjusr'
        #4. delete prjusr, prj
        #4.1 delete project collaborators
        url = '%s/_query?routing=%s' % (self.config.project_collaborator_type, pid)
        self.delete_data(qparent, url, dbase)

        #print 'Remove usrprj'
        #4.2 remove owner from user project access list
        self.remove_userprojectaccesslist(project.owner_id, pid, dbase)

        #print 'Remove prj'
        #4. delete prj
        url = '%s/%s?routing=%s' % (self.config.project_type, pid, pid)
        self.delete_data('', url, dbase)

    def index_collaborator(self, user_id, added_on, doc_version_id, project_id, dbase):
        ind = {
            "uid": user_id,
            "pid": project_id,
        }

        index_url = '%s?parent=%s&timestamp=%s' % (self.config.project_collaborator_type,
                                                    project_id,
                                                    timestamp(added_on))
        self.post_data(ind, index_url, dbase)

        #add collaborator to prj access list
        self.index_userprojectaccesslist(user_id, project_id, dbase)

    def index_userprojectaccesslist(self, user_id, project_id, dbase):
        #print 'add to user project list'
        #add to user project access list
        ind = {
            "script": "ctx._source.pidlist.contains(pid) ? (ctx.op = \"none\") : ctx._source.pidlist += pid",
            "params": {
                "pid": str(project_id)
            }
        }

        index_url = '%s/%s/_update' % ('usrprj', user_id)
        self.post_data(ind, index_url, dbase)

    def index_userprojectaccesslist_bulkreset(self, user_id, project_id_list, dbase):
        #print 'bulk reset and update user project access list'
        #bulk update ser project access list
        ind = {
                "doc": {
                    "pidlist": project_id_list
                    },
                "doc_as_upsert": True
        }

        index_url = '%s/%s/_update' % ('usrprj', user_id)
        self.post_data(ind, index_url, dbase)

    def remove_collaborator(self, user_id, doc_version_id, project_id, dbase):

        ind = {
            "filtered": {
                "query": {
                    "term": {"uid": user_id}
                    },
                "filter": {
                    "term": {"prjusr._parent": project_id}
                    }
                }
            }
        index_url = '%s/_query' % (self.config.project_collaborator_type)
        self.delete_data(ind, index_url, dbase)

        #remove collaborator from user project access list
        self.remove_userprojectaccesslist(user_id, project_id, dbase)

    def remove_userprojectaccesslist(self, user_id, project_id, dbase):
        log.msg('remove project %s from user %s' % (project_id, user_id,))

        #"script" : "if (ctx._source.pidlist.contains(pid)) { ctx._source.pidlist.remove(pid) } else { ctx.op = \"none\" }"

        #remove from user project access list
        ind = {
            "script": "ctx._source.pidlist.remove(pid)",
            "params": {
                "pid": str(project_id)
                }
            }

        index_url = '%s/%s/_update' % ('usrprj', user_id)
        self.post_data(ind, index_url, dbase)

    def index_user(self, user_id, user_guid, displayname, dbase):
        ind = {
                "name": displayname,
                "guid": user_guid,
                }
        index_url = '%s/%s' % (self.config.user_type, user_id)
        self.post_data(ind, index_url, dbase)

        #initiate user project access list
        log.msg('initialize empty project access list when user is indexed')
        ind = {"uid": user_id, "pidlist": []}
        index_url = '%s/%s' % ('usrprj', user_id)
        self.post_data(ind, index_url, dbase)

    def index_disquery(self, disquery, dbase):
        ind = {
                "title": disquery.name,
                "uid": disquery.user_id,
                "crdate": disquery.created_on.strftime(consts.YYYMMDD_DATE_FORMAT),
                "guid": disquery.guid,
                "dqid": disquery.id,
                }

        index_url = '%s/%s?timestamp=%s' % (self.config.disquery_type,
                disquery.id, timestamp(disquery.created_on))
        self.post_data(ind, index_url, dbase)

    def index_disquery_note(self, note, dbase=None):
        ind = {
                 "content": note.fragment,
                 "uid": note.created_by,
                 "crdate": note.created_on.strftime(consts.YYYMMDD_DATE_FORMAT),
                 "guid": note.guid,
                 "dqid": note.disquery_id,
              }

        if note.note_type == 'node':
            ind["ctype"] = DISQUERY_NOTE_TYPE_NODE
        else:
            ind["ctype"] = DISQUERY_NOTE_TYPE_LINK

        index_url = '%s/%s?parent=%s&routing=%s&timestamp=%s' % (
                    self.config.disquery_note_type,
                    note._id, note.disquery_id, note.disquery_id,
                    timestamp(note.created_on))

        self.post_data(ind, index_url, dbase)

    def remove_disquery(self, disquery, dbase):

        dqid = disquery.id

        #delete all disquery notes
        url = '%s/_query?routing=%s' % (self.config.disquery_note_type, dqid)
        self.delete_data({"term": {"_parent": dqid}}, url, dbase)

        #delete disquery
        url = '%s/%s?routing=%s' % (self.config.disquery_type, dqid, dqid)
        self.delete_data('', url, dbase)

    def update_disquery_name(self, disquery, dbase):
        ind = {
                "doc": {
                    "title": disquery.name,
                    "uid": disquery.user_id,
                    "crdate": disquery.created_on.strftime(consts.YYYMMDD_DATE_FORMAT),
                    "guid": disquery.guid,
                    "dqid": disquery.id,
                    },
                "doc_as_upsert": True
              }

        index_url = '%s/%s/_update' % (self.config.disquery_type, disquery.id)
        self.post_data(ind, index_url, dbase)

    @defer.inlineCallbacks
    def getUserProjectAccessList(self, current_user):
        #get user project access list
        search_url = 'http://%s:%s/%s/%s/%s' % (
                                                    self.config.host,
                                                    self.config.port,
                                                    self.config.index,
                                                    'usrprj',
                                                    current_user._id)
        jsondata = ''
        response = None
        #print search_url

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=None)

            if response.code == 200:
                jsondata = json.loads(response.body)
            else:
                log.msg(response.code)  # log response code when response is not successful
                jsondata = ''
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
        #quit, if we didnt get response for project id list
        if jsondata == '':
            defer.returnValue(jsondata)

        pidlist = ''
        if "_source" in jsondata:
            pidlist = jsondata["_source"]["pidlist"]

        defer.returnValue(pidlist)

    @defer.inlineCallbacks
    def getSubscription(self, feedid):

        #get subscription details for given feedid
        url = 'http://%s:%s/%s/%s/%s' % (
                                            self.config.feed_host,
                                            self.config.feed_port,
                                            self.config.subscription_index,
                                            self.config.subscription_type,
                                            feedid)
        jsondata = ''
        response = None
        #print url

        feedmeta = {}
        try:
            response = yield httpclient.fetch(url, method='GET', postdata=None)

            if response.code == 200:
                jsondata = json.loads(response.body)
            else:
                log.msg(response.code)  # log response code when response is not successful
                jsondata = ''

        except Exception:
            log.msg('Feed Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
        #quit, if we didnt get response
        if jsondata == '':
            defer.returnValue(feedmeta)

        feedmeta = {}
        if "_source" in jsondata:
            source = jsondata["_source"]

            feedmeta["feedid"] = jsondata["_id"]
            feedmeta["name"] = source["name"]
            feedmeta["url"] = source["url"]

            #feedmeta["update_rate"] = source["update_rate"]
            #feedmeta["ignore_ttl"] = source["ignore_ttl"]
            #feedmeta["nextrefreshdt"] = source["nextrefreshdt"]
            #feedmeta["lastupdateddt"] = source["lastupdateddt"]
            #feedmeta["fail_count"] = source["fail_count"]

        defer.returnValue(feedmeta)

    @defer.inlineCallbacks
    def getUserSubscriptionList(self, user_id):
        #get user subscription list
        url = 'http://%s:%s/%s/%s/%s' % (
                                        self.config.feed_host,
                                        self.config.feed_port,
                                        self.config.subscription_index,
                                        self.config.user_subscription_type,
                                        user_id)
        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(url, method='GET', postdata=None)

            if response.code == 200:
                jsondata = json.loads(response.body)
            else:
                log.msg(response.code)  # log response code when response is not successful
                jsondata = ''
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
        #quit, if we didnt get response for feedid list
        if jsondata == '':
            defer.returnValue(jsondata)

        feedidlist = ''
        if "_source" in jsondata:
            feedidlist = jsondata["_source"]["feedidlist"]

        defer.returnValue(feedidlist)

    @defer.inlineCallbacks
    def index_subscription(self, user_id, feedmeta, dbase):
        feed_id = feedmeta['feedid']
        log.msg('subcribe request to feed %s from user %s' % (feed_id, user_id,))

        #feed already in master list?
        fm = yield self.getSubscription(feed_id)
        if not fm:
            log.msg('feed %s subcribed for first time' % (feed_id,))
            default_update_rate = 24 * 60 * 60 * 1000       # 1 day
            nextrefreshdt = datetime.datetime.utcnow().isoformat()

            data = {
                    "name": feedmeta['name'],
                    "url": feedmeta['url'],

                    "update_rate": default_update_rate,
                    "ignore_ttl": False,
                    "nextrefreshdt": nextrefreshdt,
                    "lastupdateddt": None,
                    "fail_count": 0,
                }
            index_url = '%s/%s' % (self.config.subscription_type, feed_id,)
            self.post_feedsubscription(data, index_url, dbase)

        #update user subscription list
        self.index_usersubscriptionlist(user_id, feed_id, dbase)

        log.msg('subscribed to feed %s (user : %s)' % (feed_id, user_id,))

        defer.returnValue({"success": True, "msg": "Subscribed to feed"})

    def index_usersubscriptionlist(self, user_id, feed_id, dbase):
        log.msg('add %s to user subcription list %s' % (feed_id, user_id,))

        #    index_url = '%s/%s/_update' % (self.config.user_subscription_type, user_id)
        #    self.post_feedsubscription(data, index_url, dbase)

        #append feed id to user subcription list. (if there is no userfeed record for user, insert a new record with given feed id
        data = {
            "script": "ctx._source.feedidlist.contains(feed_id) ? (ctx.op = \"none\") : ctx._source.feedidlist += feed_id",
            "params": {
                "feed_id": str(feed_id)
            },
            "upsert": {
                "uid": user_id,
                "feedidlist": [feed_id, ]
            }
        }

        index_url = '%s/%s/_update' % (self.config.user_subscription_type, user_id)
        self.post_feedsubscription(data, index_url, dbase)

    def remove_subscription(self, user_id, feed_id, dbase):
        log.msg('remove subscription %s from user %s' % (feed_id, user_id,))

        #remove feed from user subscription list
        data = {
            "script": "ctx._source.feedidlist.remove(feedid)",
            "params": {
                "feedid": str(feed_id)
                }
            }

        index_url = '%s/%s/_update' % (self.config.user_subscription_type, user_id)
        self.post_feedsubscription(data, index_url, dbase)

    def index_watchword(self, user_id, watch_word, tag_type, dbase):
        ww = watch_word.encode('utf-8')
        tag_type = tag_type.encode('utf-8')

        log.msg("request for indexing watchword : %s type: %s" % (ww, tag_type))

        data = {
            "params": {
                "tag": ww
            },
            "upsert": {
                "uid": user_id,
                "tago": [],
                "tagp": [],
                "tagl": [],
                "tagkw": [],
                "tagcs": []
            }
        }

        validtag = False
        if tag_type == 'organization':
            data["script"] = "ctx._source.tago.contains(tag) ? (ctx.op = \"none\") : ctx._source.tago += tag"
            data["upsert"]["tago"] = [ww]
            validtag = True

        elif tag_type == 'location':
            data["script"] = "ctx._source.tagl.contains(tag) ? (ctx.op = \"none\") : ctx._source.tagl += tag"
            data["upsert"]["tagl"] = [ww]
            validtag = True

        elif tag_type == 'person':
            data["script"] = "ctx._source.tagp.contains(tag) ? (ctx.op = \"none\") : ctx._source.tagp += tag"
            data["upsert"]["tagp"] = [ww]
            validtag = True

        elif tag_type == 'keyword':
            data["script"] = "ctx._source.tagkw.contains(tag) ? (ctx.op = \"none\") : ctx._source.tagkw += tag"
            data["upsert"]["tagkw"] = [ww]
            validtag = True

        elif tag_type == 'custom':
            data["script"] = "ctx._source.tagcs.contains(tag) ? (ctx.op = \"none\") : ctx._source.tagcs += tag"
            data["upsert"]["tagcs"] = [ww]
            validtag = True

        if not validtag:
            log.msg("Request not processed for indexing watchword : Invalid tag type (%s)" % (tag_type))
            return

        index_url = '%s/%s/_update' % (self.config.watchword_type, user_id)

        #1. index watch words in main index
        self.post_data(data, index_url, dbase)

        #2. index watch words in subscription index
        self.post_feedsubscription(data, index_url, dbase)

    def remove_watchword(self, user_id, watch_word, tag_type, dbase):
        ww = watch_word.encode('utf-8')
        tag_type = tag_type.encode('utf-8')
        log.msg("request for removing watchword : %s (type: %s)" % (ww, tag_type))

        data = {
            "params": {
                "tag": ww
            }
        }

        validtag = False
        if tag_type == 'organization':
            data["script"] = "ctx._source.tago.remove(tag)"
            validtag = True
        elif tag_type == 'location':
            data["script"] = "ctx._source.tagl.remove(tag)"
            validtag = True
        elif tag_type == 'person':
            data["script"] = "ctx._source.tagp.remove(tag)"
            validtag = True
        elif tag_type == 'keyword':
            data["script"] = "ctx._source.tagkw.remove(tag)"
            validtag = True
        elif tag_type == 'custom' or tag_type == 'entity':
            data["script"] = "ctx._source.tagcs.remove(tag)"
            validtag = True

        if not validtag:
            log.msg("Request not processed for removing watchword : Invalid tag type (%s)" % (tag_type))
            return

        index_url = '%s/%s/_update' % (self.config.watchword_type, user_id)

        #1. remove watch words in main index
        self.post_data(data, index_url, dbase)

        #2. remove watch words in subscription index
        self.post_feedsubscription(data, index_url, dbase)

        #if a non-custom tag is removed, remove the custom tag with same word
        #NOTE: this logic applies only while removing watch words!!!
        if tag_type != 'custom':
            data["script"] = "ctx._source.tagcs.remove(tag)"
            #3. remove watch words in main index
            self.post_data(data, index_url, dbase)

            #4. remove watch words in subscription index
            self.post_feedsubscription(data, index_url, dbase)

    @defer.inlineCallbacks
    def search(self, term, current_user, limit=10, skip=0):

        #search for given term
        #on success, returns code:200 with results (results can be empty)
        #if search server is not accessible or parse error, returns code:500

        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }

        #escape to avoid parse exceptions
        term = term.replace("/", " ")
        if term.strip() == '':
            emptyResult["code"] = 200
            emptyResult["msg"] = 'Invalid/Empty search term'
            defer.returnValue(emptyResult)

        #get user project access list
        pidlist = yield self.getUserProjectAccessList(current_user)
        if pidlist == '':
            log.msg('user project access list is empty')
            emptyResult["code"] = 500       # project list cannot be empty!!
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        #get current user id to search only in his disqueries
        user_id = current_user._id

        #Search for given term(s) within projects where user has access
        qry = {

            "min_score": 0.01,
            "from": skip, "size": limit,
            "fields": ["title", "name", "guid", "uid", "_timestamp"],
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "fields": ["name", "title", "_all"],
                            "query": term
                        }
                    },
                    "filter": {
                        "and": [
                                 {
                                 "not":
                                 {
                                 "or": [
                                         {"term": {"_type":"docmeta"}}
                                         ]
                                        }
                                 },
                                 {
                                 "or": [
                                         {
                                         "term": {"_type": "usr"}
                                         },
                                         {
                                         "terms": {"pid": pidlist}
                                         },
                                         {
                                         "and": [
                                                 {
                                                 "term": {"_type": "dq"}
                                                 },
                                                 {
                                                 "term": {"uid": user_id}
                                                 }
                                                ]
                                         },
                                         {
                                         "and": [
                                                 {
                                                 "term": {"_type": "dqnote"}
                                                 },
                                                 {
                                                 "term": {"uid": user_id}
                                                 }
                                                ]
                                         }
                                        ]
                                 }
                                 ]
                }
                }
                },

                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 100,
                            "number_of_fragments": 1
                                },
                                "title": {}
                }
                    }
        }

        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            #defer.returnValue(jsondata)
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            try:
                rdata = strip_tags(response.body)

            except Exception:
                log.msg('html strip failed. failing back to original content')
                rdata = response.body

            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            jsondata = ''

            #if the request failed but return empty result with server error
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult)

    @defer.inlineCallbacks
    def searchForDocument(self, term, current_user, pid_filter_list=None, limit=10, skip=0):

        #Search for term within given document set
        if not term:
            #term not specified
            log.msg('term not specified in searchForDocument request')
            return

        #get user project access list
        pidlist = yield self.getUserProjectAccessList(current_user)
        if pidlist == '':
            log.msg('user project access list is empty')
            return

        #is project level filter specified?
        if pid_filter_list:
            try:
                #check whether user has access to projects specified in the filter
                alist = set(pidlist)
                flist = set(pid_filter_list)

                filtered_list = alist.intersection(flist)
                if not filtered_list:
                    log.msg('User does not have access to projects in filter listed')
                    return

                #use the filtered list
                pidlist = list(filtered_list)
            except Exception:
                log.msg('Error in searchForDocument.  %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                return

        qry = {
            "from": skip, "size": limit,
            "fields": ["guid", "title", "pid", "uid", "_timestamp"],
            "query": {
                "filtered": {
                    "query": {
                        "multi_match": {
                           "fields": ["title^2", "content"],
                            "query": term
                        }
                    },
                    "filter": {
                        "terms": {"pid": pidlist}
                      }
                    }
                },
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 100,
                            "number_of_fragments": 1
                        },
                        "title": {}
                    }
                }
        }

        search_url = 'http://%s:%s/%s/%s/_search' % (
                                                            self.config.host,
                                                            self.config.port,
                                                            self.config.index,
                                                            self.config.document_type)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='POST', postdata=json.dumps(qry))

        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
            defer.returnValue(jsondata)

        if response.code == 200:
            jsondata = json.loads(response.body)
        else:
            log.msg(response.code)  # log response code when response is not successful
            jsondata = ''

        defer.returnValue(jsondata)

    @defer.inlineCallbacks
    def getDocsByEntities(self, meta, current_user, limit=10, skip=0):

        metafilter = []
        q_pid = None
        if "location" in meta:
            metafilter.append({"terms": {"tagl.tag": [x.lower() for x in meta["location"]]}})

        if "organization" in meta:
            metafilter.append({"terms": {"tago.tag": [x.lower() for x in meta["organization"]]}})

        if "person" in meta:
            metafilter.append({"terms": {"tagp.tag": [x.lower() for x in meta["person"]]}})

        if "keyword" in meta:
            metafilter.append({"terms": {"tagkw.tag": [x.lower() for x in meta["keyword"]]}})

        #Search for the documents only within a project if pid is given
        if "pid" in meta:
            q_pid = str(meta["pid"])

        if len(metafilter) == 0:
            #no filter specified, quit
            log.msg('no filter specified to getDocsByEntities request')
            return

        #get user project access list
        pidlist = yield self.getUserProjectAccessList(current_user)
        if pidlist == '':
            log.msg('user project access list is empty')
            return

        if q_pid:
            if q_pid in pidlist:
                pidlist = [q_pid]
            else:
                #User does not have access to the project
                log.msg("User does not have access to the query project")
                return

        qry = {
                "min_score": 0.01,
                "from": skip, "size": limit,
                "fields": ["guid", "doctitle"],
                "query": {
                    "filtered": {
                        "query": {
                            "bool": {
                                "should": metafilter
                                }
                            },
                            "filter": {
                                "terms": {"pid": pidlist}
                            }
                        }
                    },
                "highlight": {
                    "pre_tags": [""],
                    "post_tags": [""],
                    "fields": {
                            "tagl.tag": {},
                            "tagp.tag": {},
                            "tago.tag": {},
                            "tagkw.tag": {}
                        }
                    }
                }

        search_url = 'http://%s:%s/%s/%s/_search' % (
                                                            self.config.host,
                                                            self.config.port,
                                                            self.config.index,
                                                            self.config.document_meta_type)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='POST', postdata=json.dumps(qry))

        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
            defer.returnValue(jsondata)

        if response.code == 200:
            jsondata = json.loads(response.body)
        else:
            log.msg(response.code)  # log response code when response is not successful
            jsondata = ''

        defer.returnValue(jsondata)

    @defer.inlineCallbacks
    def addData(self, indata, sid=None):
        
        query = indata
        
        emptyResult = {
               "created": False
            }
        if sid:
            uniquid = sid
        else:
            uniquid = random.randint(22,30000)
        
        qry = {
            "sid": uniquid,
            "name": query.get("scheme_name"),
            "funding": query.get("funding"),
            "dept": query.get("department"),
            "target":query.get("target"),
            "coverage":query.get("coverage"),
            "objectives": query.get("objectives"),
            "eligibility":query.get("eligibility"),
            "documents":query.get("documents"),
            "benefits":query.get("benefits"),
            "refurl":query.get("scheme_url")
        }


        search_url = 'http://%s:%s/%s/scheme/%s' % (self.config.host, self.config.port, self.config.index, uniquid)
        log.msg(search_url)


        jsondata = ''
        response = None
        try:
            response = yield httpclient.fetch(search_url, method='PUT', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            #defer.returnValue(jsondata)
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            emptyResult["created"] = False
            defer.returnValue(emptyResult)

        if response.code == 200 or 201:
            try:
                rdata = response.body

            except Exception:
                log.msg('html strip failed. failing back to original content')
                rdata = response.body

            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                emptyResult["created"] = True
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            jsondata = ''

            #if the request failed but return empty result with server error
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            emptyResult["created"] = False
            defer.returnValue(emptyResult)

    @defer.inlineCallbacks
    def searchv2(self, current_user, term=None, terms=[], limit=10, skip=0):

        #search for given term
        #on success, returns code:200 with results (results can be empty)
        #if search server is not accessible or parse error, returns code:500
        print '1111111111'
        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }


        if not term or term.strip() == '':
            term = "*"
        term = term.replace("/", " ")

        str_list = []
        for x in terms:
            str_list.append(
                          {
                             "query": {
                                "query_string": {
                                   "query": x
                                }
                             }
                          }
            )
 


        #Search for given term(s) within projects where user has access
        qry = {

           "highlight":{
                "fields":{
                    "eligibility" : {},
                    "benefits" : {},
                    "target" : {},
                    "objectives" : {}
                }
            },
            "min_score": 0.01,
            "from": skip, "size": limit,
            "sort": [
                {
                    "_score": {
                                "order": "desc"
                              }
                }
            ],
            "_source": ["name", "dept", "funding", "target", "objectives", "eligibility", "benefits", "coverage","refurl", "documents"],
            "query": {
                "filtered": {
                   "query": {
                             "bool": {
                                      "should": [
                                                 {
                                                  "query_string": {"query": term}
                                                  }
                                                 ]
                                      }
                },
                "filter": {
                    "and": {
                       "filters": str_list,
                       "_cache": "true"
                    }
                      }
                             
                }
                }
        }

        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None
        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            #defer.returnValue(jsondata)
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            try:
                rdata = response.body

            except Exception:
                log.msg('html strip failed. failing back to original content')
                rdata = response.body

            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            jsondata = ''

            #if the request failed but return empty result with server error
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult)


    @defer.inlineCallbacks
    def getDocWithGuid(self, dGuids):

        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }

        if not dGuids:
            emptyResult["code"] = 200
            emptyResult["msg"] = 'No documents'
            defer.returnValue(emptyResult)

        dList = [{"term": {"doc.guid": x}} for x in dGuids]

        qry = {
                "fields": ["title", "content"],
                "sort": {"crdate": {"order": "desc"}},
                "query": {"bool": {"should": dList}}
        }

        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult)


    @defer.inlineCallbacks
    def getDocMetaWithdid(self, dids):

        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }

        if not dids:
            emptyResult["code"] = 200
            emptyResult["msg"] = 'No documents'
            defer.returnValue(emptyResult)

        dList = [{"term": {"docmeta.did": x}} for x in dids]

        qry = {
                "fields": ["topics", "did"],
                "sort": {"crdate": {"order": "desc"}},
                "query": {"bool": {"should": dList}}
        }

        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult)


    @defer.inlineCallbacks
    def getEventWithGuid(self, dGuids):

        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }

        if not dGuids:
            emptyResult["code"] = 200
            emptyResult["msg"] = 'No documents'
            defer.returnValue(emptyResult)

        dList = [{"term": {"docmeta.guid": x}} for x in dGuids]

        qry = {
                "_source": ["events", "did"],
                "size": 100,
                "sort": {"crdate": {"order": "desc"}},
                "query": {"bool": {"should": dList}}
        }

        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult)


    @defer.inlineCallbacks
    def getSimilarDocsByTitle(self, title, dGuid, show_all):

        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }

        if not title:
            emptyResult["code"] = 200
            emptyResult["msg"] = 'No documents'
            defer.returnValue(emptyResult)

        start_date = date.today().strftime("%Y-%m-%d")
        end_date = None
        if not show_all:
            edDate = date.today()-timedelta(days=14)
            end_date = edDate.strftime("%Y-%m-%d")

        qry = {
               "fields": [
                  "title",
                  "crdate",
                  "guid",
                  "_score",
                  "content"
               ],
               "query": {
                  "filtered": {
                     "query": {
                        "bool": {
                           "should": {
                              "text": {
                                 "doc.title": title
                              }
                           },
                           "must_not": {
                              "term": {
                                 "doc.guid": dGuid
                              }
                           }
                        }
                     },
                     "filter": {
                        "bool": {
                           "should": [
                              {
                                 "range": {
                                    "crdate": {
                                       "gte": end_date,
                                       "lte": start_date
                                    }
                                 }
                              }
                           ],
                           "_cache": "true"
                        }
                     }
                  }
               }
        }

        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult)     


    @defer.inlineCallbacks
    def getEventsWithEntity(self, entity):

        qry = {
                  "_source": ["events", "tago", "tagp", "tagkw"],
                  "size": 100,
                  "query": {
                        "bool": {
                            "must": [
                                {
                                    "query_string": {
                                            "default_field": "docmeta.events.entities.tag",
                                            "query": entity.lower()
                                    }
                                }
                            ]
                        }
                  }
        }


        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                return
            else:
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            return


    @defer.inlineCallbacks
    def getEventsWithTerm(self, term):

        qry = {
                  "_source": ["events", "tago", "tagp", "tagkw"],
                  "size": 100,
                  "query": {
                        "filtered":{
                                "query":{
                                        "has_parent":{
                                                "parent_type":"doc",
                                                "query":{
                                                        "bool":{
                                                                "must":[
                                                                    {
                                                                        "query_string":{
                                                                            "default_field":"doc.content",
                                                                            "query":term
                                                                        }
                                                                    }
                                                                ]
                                                        }
                                                 }
                                         }
                                 }
                         }
                  }
        }


        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            returnValue

        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                return
            else:
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            return


    @defer.inlineCallbacks
    def getSimilarTerms(self, term):

        qry = {
            "query":{
                "bool":{
                    "must":[
                        {
                            "query_string":{
                                "default_field":"doc.content",
                                "query":term
                            }
                        }
                    ]
                }
            },
            "aggregations":{
                "similarTerms":{
                    "significant_terms":{
                        "field":"content"
                    }
                }
            }
        }


        search_url = 'http://%s:%s/%s/_search' % (self.config.host, self.config.port, self.config.index)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                return
            else:
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            return


    @defer.inlineCallbacks
    def getAllReviews(self, feature=None, guid=None, limit=100):

        emptyResult = {
                    u'hits': {u'hits': [], u'total': 0, u'max_score': None},
                    u'took': 0,
                    u'timed_out': False
        }

        qry = {
                "_source": ["crdate", "content", "rating"],
                "sort": {"crdate": {"order": "desc"}},
                "size": limit
        }

        if feature:
            qry['query'] = {
                            "match_phrase" : {
                                "content" : feature
                            }
                           }
            qry['highlight'] = {
                                "fields" : {
                                           "content" : {
                                               "number_of_fragments": 0
                                            }
                                }
                               }

        if feature or guid:
            qry['query'] =  {
                          "bool":{
                             "must":[
                                 {
                                  "query_string":
                                      {
                                       "default_field":"doc.content",
                                       "query":feature
                                      }
                                 }
                             ]
                          }
                         }
            if feature:
                qry['query']['bool']['must'].append({
                                                    "query_string": {
                                                        "default_field": "content",
                                                        "query": feature
                                                    }
                                                   })
            if guid:
                qry['query']["bool"]["must"].append({
                                                    "term": {
                                                        "guid": guid
                                                    }
                                                   })
        search_url = 'http://%s:%s/%s/%s/_search' % (self.config.voc_host, self.config.voc_port, self.config.voc_index, self.config.review_type)
        log.msg(search_url)

        jsondata = ''
        response = None

        try:
            response = yield httpclient.fetch(search_url, method='GET', postdata=json.dumps(qry))
        except Exception:
            log.msg('Search Server not accessible - %s : %s' % (
                                                        sys.exc_info()[0],
                                                        traceback.
                                                        format_exc()))
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server is down'
            defer.returnValue(emptyResult)

        if response.code == 200:
            rdata = response.body
            try:
                jsondata = json.loads(rdata)
            except Exception:
                log.msg('Search result JSON invalid - %s : %s' % (sys.exc_info()[0], traceback.format_exc()))
                jsondata = ''

            # if the request was successful but there is not data, return empty result
            if jsondata == '':
                emptyResult["code"] = 200
                emptyResult["msg"] = ''     # no msg
                defer.returnValue(emptyResult)
            else:
                jsondata['code'] = 200
                defer.returnValue(jsondata)

        else:
            log.msg(response.code)  # log response code when response is not successful
            emptyResult["code"] = 500
            emptyResult["msg"] = 'Search Server not accessible'
            defer.returnValue(emptyResult) 
