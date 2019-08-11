"""
dict 项目用于数据处理
"""

import pymysql
import hashlib
import time


# 编写功能类  提供给服务端使用
class Database:
    def __init__(self,host = 'localhost',port = 3306,
                 user = 'root',
                 passwd = '123456',
                 database = 'dict',
                 charset = 'utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(host = self.host,port = self.port,
                                  user = self.user,passwd = self.passwd,
                                  database = self.database,charset = self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.cur.close()
        self.db.close()

    # 处理注册
    def register(self,name,passwd):
        sql = "select * from user where name = '%s';"%name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False

        # 加密处理
        hash = hashlib.md5((name+"the-salt").encode())
        hash.update(passwd.encode())
        sql = "insert into user (name,passwd) values(%s,%s);"

        try:
            self.cur.execute(sql,[name,hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    # 处理登录
    def login(self,name,passwd):
        sql = "select * from user where name = '%s';" % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if not r:
            return False
        hash = hashlib.md5((name + "the-salt").encode())
        hash.update(passwd.encode())
        if r[2] != hash.hexdigest():
            return False
        else:
            return True

    # 插入历史记录
    def insert_history(self,name,word):
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values (%s,%s,%s)"
        try:
            self.cur.execute(sql,[name,word,tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    # 查单词
    def query(self,word):
        sql = "select mean from words where word = '%s';"%word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    # 查历史记录
    def history(self,name):
        sql = "select word from hist where name = '%s';"%name
        self.cur.execute(sql)
        r = self.cur.fetchall()
        if r:
            return r





