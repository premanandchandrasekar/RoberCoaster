import mimetypes

FETCH_RSS_FEEDS = 'fetch_rss_feeds'

CACHE_INVALIDATION_ROUTING_KEY = 'cache:invalidation:pubsub'
SESSION_ID_PREFIX = 'ssid'


REFETCH_DATA_ON_DEVICE_ROUTING_KEY = 'refetch_data'
PROJECT_LAYERS_SHARED_ROUTING_KEY = 'project_layers_shared'

S3_FILE_DOWNLOADS_LOCATION = '../s3_downloads/'

UNIX_FORMAT = '%s'
DT_FORMAT = '%c'
YYYMMDD_DATE_FORMAT = '%Y%m%d'

MIMETYPE_MAP = {
    'application/pdf': 'pdf',
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'image/gif': 'gif',
    'image/tiff': 'tiff',
    'image/bmp': 'bmp',
    'audio/x-aac': 'aac',
    'text/html': 'html',
    'application/xhtml+xml': 'html',
    'audio/x-wav': 'wav',
    'audio/mpeg': 'mp3',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/vnd.ms-powerpoint': 'ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    'text/plain': 'txt',
    'application/xml': 'xml',
    'text/xml': 'xml',
    'text/x-opml': 'opml'
}

REVERSE_MIMETYPE_MAP = dict((x[1], x[0]) for x in MIMETYPE_MAP.items())
REVERSE_MIMETYPE_MAP['jpeg'] = 'image/jpeg'
REVERSE_MIMETYPE_MAP['htm'] = 'text/html'


UPLOAD_EXTENSIONS = []
for mt in MIMETYPE_MAP.keys():
    UPLOAD_EXTENSIONS.extend(mimetypes.guess_all_extensions(mt))

UPLOAD_EXTENSIONS.extend([".aac", ".m4a", ".bmp", ".txt", ".xml", ".opml"])
UPLOAD_EXTENSIONS = frozenset(UPLOAD_EXTENSIONS)
#UPLOAD_EXTENSIONS.extend([".aac", ".m4a"])
#UPLOAD_EXTENSIONS = ['.aac', '.html', '.pdf', '.jpg', '.png', '.gif', '.tiff',
#                     '.bmp', '.m4a']
del mimetypes

secret_key = 'XjnDSQQyOZK9WdTZ0tOiTkhX2D01QmJEfGZp/RNk='

feed_secret_key = '8UqSgI3gRHC7vnatoPPg3KJC52ydf0KwnbEnU6PgS+U='
YYYMMDD_DATE_FORMAT = '%Y%m%d'

TASK_EXCHANGE_NAME = 'DQ_TASK_EXCHANGE'
NOTIFICATIONS_EXCHANGE_NAME = 'DQ_PUBSUB_NOTIFICATIONS'

PROCESS_MATCHED_FEED = 'process_matched_feed'
FETCH_RSS_FEEDS = 'fetch_rss_feeds'

private_key = 'tataatsudisquery'

global_prj = 'cb281366-4662-4e52-b4ff-e8719a5a066a'