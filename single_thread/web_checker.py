from model import *
import requests, time
import pandas as pd
from pprint import pprint

n_epochs = 5 # request n_epochs time each time 

class Checker:
	def __init__(self):
		self.sess = requests.session()

	def run(self, url):
		for i in range(n_epochs): 
			try:
				r = self.sess.get(url, timeout=5)
			except:
				data = {
					'time_response': -1,
					'status_code': 408,
					'timestamp' : time.time()
				}
			else:
				data = {
					'time_response': r.elapsed.total_seconds(),
					'status_code': r.status_code,
					'timestamp' : time.time()
				}
			finally:
				yield data
				time.sleep(3)
				if data['status_code'] == 200:
					break
			
class WebChecker:
	def __init__(self):
		self.url = URL()
		self.user_url = UserURL()
		self.checker = Checker()
		self.event = Event()

	def get_data(self):
		user_urls = pd.DataFrame.from_records(list(self.user_url.get()), columns=['user_id', 'url_id'])
		urls = pd.DataFrame.from_records(list(self.url.get()), columns=['id', 'url'])

		for id, url in urls.iterrows():
			print url.url
			for result in self.checker.run(url.url):
				for user_id in user_urls[user_urls.url_id == url.id]['user_id']:
					event = {
						'user_id' : user_id.astype(int),
						'url_id' : url.id,
						'_index' : 'webassistant3',
						'_type' : 'webassistant3'
						
					}
					event.update(result)
					yield event

	def run(self):
		reload()
		# reset_database()
		self.event.insert(self.get_data())

if __name__ == '__main__':
	WebChecker().run()
	# Checker().run('http://vnist.vn')
