from config import Config

config = Config()

from elasticsearch import helpers

data = [{
	'_index' : 'webassistant',
	'_type' : 'type',
	'msg' : 'test'
}]
helpers.bulk(config.es, data)

