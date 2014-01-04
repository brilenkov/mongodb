#BOT_NAME = 'app'
#BOT_VERSION = '1.0'

SPIDER_MODULES = ['mongodb.spiders']
NEWSPIDER_MODULE = 'mongodb.spiders'
DEFAULT_ITEM_CLASS = 'mongodb.items.BusDirItem'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

'''
ITEM_PIPELINES = [
  'scrapymongodb.MongoDBPipeline',
]

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'scrapy'
MONGODB_COLLECTION = 'items'
MONGODB_UNIQ_KEY = 'url'
MONGODB_ITEM_ID_FIELD = '_id'
MONGODB_SAFE = True
'''

ITEM_PIPELINES = [
    #'scrapy_mongodb.MongoDBPipeline',
    'mongodb.pipelines.MongoDBPipeline',
    'mongodb.pipelines.CsvExportPipeline'
]
WEBSERVICE_ENABLED = True
EXTENSIONS = {
    'scrapy.contrib.corestats.CoreStats': 500,
    'scrapy.webservice.WebService': 500,
    #'scrapy.telnet.TelnetConsole': 500,
}
CONCURRENT_REQUESTS_PER_DOMAIN = 10
CONCURRENT_REQUESTS = 10
RANDOMIZE_DOWNLOAD_DELAY = False
DOWNLOAD_DELAY = 0
#LOG_LEVEL = 'WARNING'
LOG_LEVEL = 'DEBUG'
LOG_FILE   = 'mongodb.log'

#from pymongo import MongoClient
#uri = 'mongodb://brilenkov:123456@ds061298.mongolab.com:61298/scrapy'
#client = pymongo.MongoClient(uri)

MONGODB_CONN = 'mongodb://brilenkov:123456@ds061298.mongolab.com:61298/scrapy'
