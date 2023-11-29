# 基础类，作用配置默认的请求基类，配置程序的访问控制，如果没有登陆，则跳转到登陆页面
import tornado.web

# 所有请求都会通过这个基类来检查
class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        print("Error:{}".format(status_code))
        self.write("Error:{}".format(status_code))
    
    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if isinstance(username, bytes):
            return username.decode(encoding = "utf-8")
        return None

# 入口检查类，也是默认页入口
class EnterHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect("/main")