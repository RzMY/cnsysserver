# 服务启动模块
import sys
import tornado.ioloop
import tornado.options

# options是tornado中用于配置整个框架的基类
import tornado.httpserver
from tornado.options import define, options, parse_command_line

# 导入所有程序的模块
from application import app
# 定义端口号
define("port", default = 10086, type = int, help = "Server Listen On The Given Ports")
# cmd python server.py --help
# cmd python server.py --port = 10086

def main():
    parse_command_line()# 接收控制端的输入内容参数值--port=10086
    print("ZL HTTPServer Runing On Port {} ...".format(options.port))
    print("Stop The ZL HTTPServer With Ctrl + C")
    # 将程序app部署到HTTPServer中
    httpserever = tornado.httpserver.HTTPServer(app)
    httpserever.bind(options.port,reuse_port=False)
    httpserever.start(0)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == "__main__":
    main()
    