# Create database

from config import Config
from elasticsearch import helpers
config = Config()

class User:
    def __init__(self):
        pass

    # def migrate(self):
    #     config.mysql_cur.execute('''
    #         CREATE TABLE `users` (
    #             `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    #             `username` TEXT,
    #             `name` TEXT,
    #             `email` TEXT,
    #             `password` TEXT,
    #             `authentication_token` TEXT,
    #             `expired_time` datetime,
    #             `group_id` int(11),
    #             `lock` tinyint(1)
    #         )
    #     ''')
    #     config.mysql_conn.commit()

    def get(self):
        conn, cur = config.get_mysql()
        cur.execute('SELECT * FROM `users`')
        result = cur.fetchall()
        config.append_mysql(conn, cur)
        return result

class Url:
    def __init__(self):
        pass

    # def migrate(self):
    #     config.mysql_cur.execute('''
    #         CREATE TABLE `urls` (
    #             `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    #             `url` varchar(255) UNIQUE,
    #             `status` tinyint(1)
    #         )
    #     ''')
    #     config.mysql_conn.commit()

    def get(self):
        conn, cur = config.get_mysql()
        cur.execute('SELECT id, url FROM `urls`')
        result = cur.fetchall()
        config.append_mysql(conn, cur)
        return result
        # return ((1, u'http://vnist.vn'),)

    def count(self):
        conn, cur = config.get_mysql()
        cur.execute('SELECT COUNT(*) FROM `urls`')
        result = cur.fetchone()[0]
        config.append_mysql(conn, cur)
        return result

    def get_user_url(self):
        conn, cur = config.get_mysql()
        cur.execute('''SELECT u.id,m.user_id FROM masters AS m, urls AS u, master_urls AS mu WHERE mu.master_id=m.id AND mu.url_id=u.id''')
        result = cur.fetchall()
        config.append_mysql(conn, cur)
        return result

    def update_status(self, status, url_id):
        assert status == 0 or status == 1
        conn, cur = config.get_mysql()
        cur.execute('UPDATE `urls` SET status = %d WHERE id = %s' % (status, url_id))
        conn.commit()
        config.append_mysql(conn, cur)

class Master:
    def __init__(self):
        pass

    # def migrate(self):
    #     config.mysql_cur.execute('''
    #         CREATE TABLE `masters` (
    #             id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    #             user_id int(11),
    #             url TEXT,
    #             title TEXT,
    #             FOREIGN KEY (user_id) REFERENCES users(id)
    #         )
    #     ''')
    #     config.mysql_conn.commit()

    def get(self):
        conn, cur = config.get_mysql()
        cur.execute('SELECT * FROM `masters`')
        result = cur.fetchall()
        config.append_mysql(conn, cur)
        return result
        # return ((1, 1),)

class MasterUrl:
    def __init__(self):
        pass

    # def migrate(self):
    #     config.mysql_cur.execute('''
    #         CREATE TABLE `master_urls` (
    #             master_id int(11),
    #             url_id int(11),
    #             title TEXT,
    #             FOREIGN KEY (master_id) REFERENCES masters(id),
    #             FOREIGN KEY (url_id) REFERENCES urls(id),
    #             PRIMARY KEY (master_id, url_id)
    #         )
    #     ''')
    #     config.mysql_conn.commit()

    def get(self):
        conn, cur = config.get_mysql()
        cur.execute('SELECT * FROM `master_urls`')
        result = cur.fetchall()
        config.append_mysql(conn, cur)
        return result
        # return ((1, 1),)


def reload():
    config.reload()        

def reset_database():
    conn, cur = config.get_mysql()
    es = config.get_es()
    cur.execute('DELETE FROM `master_urls`')
    cur.execute('DELETE FROM `masters`')
    cur.execute('DELETE FROM `users`')
    cur.execute('DELETE FROM `urls`')
    conn.commit()
    es.delete(index='webassistant3', ignore=[400, 404])
    es.create(index='webassistant3', ignore=[400, 404])
    config.append_mysql(conn, cur)
    config.append_es(es)


class Event:
    def __init__(self):
        pass

    def insert(self, event_generator):
        es = config.get_es()
        helpers.bulk(es, event_generator)
        config.append_es(es)

    def had_first_event(self, user_id, url_id):
        es = config.get_es()
        query = {
            'query': {
                'match': {'user_id': user_id},
                'match': {'url_id': url_id}
            }
        }
        if es.count(index='webassistant3', doc_type='event', body=query)['count']:
            result = True
        else:
            result = False
        config.append_es(es)
        return result

if __name__ == '__main__':
    from elasticsearch import Elasticsearch
    es = Elasticsearch(['192.168.1.65:9200'])
    # es.delete(index='webassistant3', ignore=[400, 404])
    es.create(index='webassistant3', ignore=[400, 404])
    # Event().first_event(33, 1)