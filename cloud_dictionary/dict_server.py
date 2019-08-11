"""
dict 服务端
处理请求逻辑
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from operation_db import *

# 全局变量

HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

# 处理注册
def do_register(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name, passwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")

# 处理登录
def do_login(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")

# 处理查询  Q name word
def do_query(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    # 插入历史记录
    db.insert_history(name,word)

    # 查单词
    mean = db.query(word)
    if not mean:
        c.send("查无此词".encode())
    else:
        msg = "%s : %s"%(word,mean)
        c.send(msg.encode())

# 处理历史查询  H name
def do_history(c,db,data):
    tmp = data.split(" ")
    name = tmp[1]
    # 查询历史记录
    history = db.history(name)
    if not history:
        c.send("暂无历史记录".encode())
    else:
        if len(history)<= 10:
            for item in history:
                msg = item[0] + ' '
                c.send(msg.encode())
        else:
            history2 = history[len(history):-11:-1]
            for item in history2:
                msg = item[0]+' '
                c.send(msg.encode())

def do_request(c,db):
    db.create_cursor()    # 生成游标 db.cur
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit("客户端退出")
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_history(c,db,data)

def main():
    # 创建数据库连接对象
    db = Database()
    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    # 循环等待客户端连接
    print("Listen the port 8000")
    while True:
        try:
            c,addr = s.accept()
            print("Connect from:",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        p = Process(target=do_request,args = (c,db))
        p.daemon = True
        p.start()






if __name__ == "__main__":
    main()
