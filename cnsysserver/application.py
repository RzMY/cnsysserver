# 整个程序模块，用于加载各子程序或子模块
import tornado.web
import tornado.httpserver
from tornado.web import URLSpec

from conf.base import BaseHandler,EnterHandler
from conf.conf import *

# 导入定义的controller
from controller.loginC import LoginHandler
# 定义并设置应用的通用配置
# 放置所有的请求地址及请求对应的视图

handlers = list()

# 配置地址对应的路由
# 默认地址是/
# http://localhost:10086/
handlers.extend([
    URLSpec("/",EnterHandler,name="enterPoint"),
    URLSpec("/login",LoginHandler,name="loginPoint"),
])

# 将路由放置到application中
app = tornado.web.Application(handlers=handlers,**setting)