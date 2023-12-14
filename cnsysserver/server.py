# 服务启动模块
import sys
import tornado.ioloop
import tornado.options
import conf.conf
import datetime
# options是tornado中用于配置整个框架的基类
import tornado.httpserver
from tornado.options import define, options, parse_command_line

# 导入所有程序的模块
from application import app
# 定义端口号

define("port", default = 10086, type = int, help = "Server Listen On The Given Ports")
# cmd python server.py --help
# cmd python server.py --port = 10086

def check_inactive_users():
    db = conf.conf.db
    cursor = db.cursor()
    one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
    sql = """SELECT username FROM session WHERE (last_active < %s OR (last_active IS NULL AND session_id IS NOT NULL))"""
    cursor.execute(sql, (one_minute_ago,))
    inactive_users = cursor.fetchall()
    for user in inactive_users:
        print("用户{}超时下线".format(user[0]))
        sql = """UPDATE session SET session_id = NULL, last_active = NULL WHERE username = %s"""
        cursor.execute(sql, (user,))
        db.commit()
    if len(inactive_users) > 0:
        print("清理超时用户完成 当前时间：{}".format(datetime.datetime.now()))
    cursor.close()

def main():
    parse_command_line()# 接收控制端的输入内容参数值--port=10086
    print("ZL HTTPServer Runing On Port {} ...".format(options.port))
    print("Stop The ZL HTTPServer With Ctrl + C")
    # 将程序app部署到HTTPServer中
    httpserever = tornado.httpserver.HTTPServer(app)
    httpserever.bind(options.port,reuse_port=False)
    httpserever.start() # 0 是多进程 默认1个进程，其他数字是指定的进程数
    check_inactive_users()
    tornado.ioloop.PeriodicCallback(check_inactive_users, 60000).start() # 每隔60秒执行一次
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == "__main__":
    main()