# Create database

from config import Config
from elasticsearch import helpers
config = Config()

class User:
    def __init__(self):
        pass

    def migrate(self):
        config.mysql_cur.execute('''
            CREATE TABLE `users` (
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

    def get(self):
        config.mysql_cur.execute('SELECT * FROM `users`')
        return config.mysql_cur.fetchall()

class Url:
    def __init__(self):
        pass

    def migrate(self):
        config.mysql_cur.execute('''
            CREATE TABLE `urls` (
                `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                `url` varchar(255) UNIQUE,
                `status` tinyint(1)
            )
        ''')
        config.mysql_conn.commit()

    def get(self):
        config.mysql_cur.execute('SELECT id, url FROM `urls`')
        return config.mysql_cur.fetchall()
        # return ((1, u'http://vnist.vn'),)

    def count(self):
        config.mysql_cur.execute('SELECT COUNT(*) FROM `urls`')
        return config.mysql_cur.fetchone()[0]

    def get_user_url(self):
    	config.mysql_cur.execute('''SELECT u.id,m.user_id FROM masters AS m, urls AS u, master_urls AS mu WHERE mu.master_id=m.id AND mu.url_id=u.id''')
        return config.mysql_cur.fetchall()

    def update_status(self, status, url_id):
        assert status == 0 or status == 1
        config.mysql_cur.execute('UPDATE `urls` SET status = %d WHERE id = %s' % (status, url_id))
        config.mysql_conn.commit()

class Master:
    def __init__(self):
        pass

    def migrate(self):
        config.mysql_cur.execute('''
            CREATE TABLE `masters` (
                id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                user_id int(11),
                url TEXT,
                title TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        config.mysql_conn.commit()

    def get(self):
        config.mysql_cur.execute('SELECT * FROM `masters`')
        return config.mysql_cur.fetchall()
        # return ((1, 1),)

class MasterUrl:
    def __init__(self):
        pass

    def migrate(self):
        config.mysql_cur.execute('''
            CREATE TABLE `master_urls` (
                master_id int(11),
                url_id int(11),
                title TEXT,
                FOREIGN KEY (master_id) REFERENCES masters(id),
                FOREIGN KEY (url_id) REFERENCES urls(id),
                PRIMARY KEY (master_id, url_id)
            )
        ''')
        config.mysql_conn.commit()

    def get(self):
        config.mysql_cur.execute('SELECT * FROM `master_urls`')
        return config.mysql_cur.fetchall()
        # return ((1, 1),)


def reload():
    config.reload()        

def reset_database():
    config.mysql_cur.execute('DELETE FROM `master_urls`')
    config.mysql_cur.execute('DELETE FROM `masters`')
    config.mysql_cur.execute('DELETE FROM `users`')
    config.mysql_cur.execute('DELETE FROM `urls`')
    config.mysql_conn.commit()
    config.es.indices.delete(index='webassistant3', ignore=[400, 404])
    config.es.indices.create(index='webassistant3', ignore=[400, 404])

class Event:
    def __init__(self):
        pass

    def insert(self, event_generator):
        helpers.bulk(config.es, event_generator)
        
if __name__ == '__main__':
    import os

    # User().migrate()
    # Url().migrate()
    # Master().migrate()
    # MasterUrl().migrate()
    
    reset_database()
    os.system('python reset_database.py')

    print User().get()
    print Url().get()
    print Master().get()
    print MasterUrl().get()
