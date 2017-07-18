# Create database

from config import Config
from elasticsearch import helpers
config = Config()

class User:
	def __init__(self):
		pass

	def migrate(self):
		config.mysql_cur.execute('''
			CREATE TABLE `user` (
				`id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
				`username` TEXT,
				`name` TEXT,
				`email` TEXT,
				`password` TEXT,
				`authentication_token` TEXT,
				`expired_time` datetime,
				`group_id` int(11),
				`lock` tinyint(1)
			)
		''')
		config.mysql_conn.commit()

	def create(self):

		config.mysql_cur.execute('''
			INSERT INTO `user` VALUES (
				10, 'haidv', 'Duong Van Hai', 'haidv@vnist.vn', 'nghia123', '', 0, 1, 0 
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `user` VALUES (
				20, 'thanhlt', 'Le Tien Thanh', 'thanhlt@vnist.vn', 'nghia123', '', 0, 1, 0 
			)
		''')
		config.mysql_conn.commit()



class URL:
	def __init__(self):
		pass

	def migrate(self):
		config.mysql_cur.execute('''
			CREATE TABLE `url` (
				`id` int(11) PRIMARY KEY  NOT NULL AUTO_INCREMENT,
				`url` TEXT
			)
		''')
		config.mysql_conn.commit()

	def create(self):

		config.mysql_cur.execute('''
			INSERT INTO `url` VALUES (
				1, 'http://vnist.vn'
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `url` VALUES (
				2, 'https://beta.vntrip.vn'
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `url` VALUES (
				3, 'https://vinhphuc1000.vn'
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `url` VALUES (
				4, 'https://lab.vnist.vn'
			)
		''')
		config.mysql_conn.commit()	

	def get(self):
		config.mysql_cur.execute('SELECT * FROM `url`')
		return config.mysql_cur.fetchall()
		# return ((1, u'http://vnist.vn'),)


class UserURL:
	def __init__(self):
		pass

	def migrate(self):
		config.mysql_cur.execute('''
			CREATE TABLE `user_url` (
				user_id int(11),
				url_id int(11),
				FOREIGN KEY (user_id) REFERENCES user(id),
				FOREIGN KEY (url_id) REFERENCES url(id),
				PRIMARY KEY (user_id, url_id)
			)
		''')
		config.mysql_conn.commit()

	def create(self):
		
		config.mysql_cur.execute('''
			INSERT INTO `user_url` VALUES (
				10, 1
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `user_url` VALUES (
				20, 1
			)
		''')

		config.mysql_cur.execute('''
			INSERT INTO `user_url` VALUES (
				10, 2
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `user_url` VALUES (
				10, 3
			)
		''')
		config.mysql_cur.execute('''
			INSERT INTO `user_url` VALUES (
				20, 4
			)
		''')

		config.mysql_conn.commit()

	def get(self):
		config.mysql_cur.execute('SELECT * FROM `user_url`')
		return config.mysql_cur.fetchall()
		# return ((1, 1),)

def reload():
	config.reload()		

def delete():
	config.mysql_cur.execute('DELETE FROM `user_url`')
	config.mysql_cur.execute('DELETE FROM `user`')
	config.mysql_cur.execute('DELETE FROM `url`')
	config.mysql_conn.commit()


def reset_database():
    config.es.indices.delete(index='webassistant3', ignore=[400, 404])
    config.es.indices.create(index='webassistant3', ignore=[400, 404])


class Event:
	def __init__(self):
		pass

	def insert(self, event_generator):
		helpers.bulk(config.es, event_generator)
		


if __name__ == '__main__':
	delete()
	URL().create()
	User().create()
	UserURL().create()
