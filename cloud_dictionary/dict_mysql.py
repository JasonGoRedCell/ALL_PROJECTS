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

with open('dict.txt') as f:
    while True:
        a = f.readline()
        word = re.search('\S+', a).group()
        first_letter = word[0].lower()
        try:
            explanation = re.search(r"\s.+",a).group()
            sql = "insert into dict_1 values(%s,%s,%s);"
            cur.execute(sql, [first_letter, word, explanation])
            db.commit()
        except Exception:
            pass
        if not a:
            break





