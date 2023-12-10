import tornado.web
from conf.base import BaseHandler,EnterHandler

class LoginOutHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db
        
    def prepare(self):
        self.cursor = self.db.cursor()
        
    def on_finish(self):
        self.cursor.close()
        
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("userName")
        self.redirect("/login")