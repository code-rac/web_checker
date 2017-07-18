import pymysql

data = {
    'users' : [
        [1, 'haidv12', 'Duong Van Hai', 'haidv@vnist.vn', 'nghia123', '', 0, 1, 0],
        [2, 'thanhlt', 'Le Tien Thanh', 'thanhlt@vnist.vn', 'nghia123', '', 0, 1, 0],
        [3, 'hieult', 'Ly Trung Hieu', 'hieult@vnist.vn', 'nghia123', '', 0, 1, 0],
    ],
    'urls' : [
        [1, 'http://vnist.vn', 1],
        [2, 'http://vinhphuc.gov.vn/Pages/default.aspx', 1],
        [3, 'https://mail.vnist.vn', 1],
        [4, 'https://lab.vnist.vn', 0],
        [5, 'https://cho.thanh.vn', 0],
        [6, 'http://192.168.1.16', 0]
    ],
    'masters' : [
        [1, 1, 'http://vnist.vn', 'VNIST website'],
        [2, 2, 'http://vnist.vn', 'VNIST website'],
        [3, 1, 'http://vinhphuc.gov.vn', 'Vinh Phuc'],
        [4, 3, 'https://cho.thanh.vn', 'Do Tu Tai'],
    ],
    'master_urls': [
        [1, 1, 'trang chu vnist'],
        [1, 3, 'mail vnist'],
        [1, 4, 'lab vnist'],
        [2, 1, 'trang chu vnist'],
        [2, 3, 'mail vnist'],
        [2, 4, 'lab vnist'],
        [3, 2, 'trang chu vinh phuc'],
        [4, 5, 'trang linh tinh'],
        [4, 6, 'trang linh tinh 2'],
    ]
}

conn = pymysql.connect(host='192.168.1.65', user='root', password='vnistadmin', db='webassistant3', charset='utf8mb4')
cur = conn.cursor()

for tbl_name in ['users', 'urls', 'masters', 'master_urls']:
    for row in data[tbl_name]:
        query =  ' '.join(('INSERT INTO %s VALUES' % tbl_name, str(row).replace('[', '(').replace(']', ')')))
        try:
            cur.execute(query)
        except:
            print(query)
            raise
conn.commit()