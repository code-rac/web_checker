import pymysql

HOST = '192.168.1.65'
conn = pymysql.connect(host=HOST, user='root', password='vnistadmin', db='webassistant3', charset='utf8mb4')
cur = conn.cursor()


print cur.fetchall()