import pymysql
import re

# 链接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='123456',
                     database='dict',
                     charset='utf8')
# 　获取游标
cur = db.cursor()

f = open('dict.txt')
sql = 'insert into words (word,mean) values (%s,%s);'
for line in f:
    tup =re.findall(r"(\w+)\s+(.*)",line)[0]
    try:
        cur.execute(sql,tup)
        db.commit()
    except Exception:
        db.rollback()
f.close()
cur.close()
db.close()