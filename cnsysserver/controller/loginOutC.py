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
        # 注销用户
        self.clear_cookie("userName")
        self.clear_cookie("session_id")
        # 清除数据库中的session_id
        sql = """UPDATE session SET session_id = NULL, last_active = NULL WHERE username = %s"""
        self.cursor.execute(sql, (self.get_current_user(),))
        self.db.commit()
        self.redirect("/login")