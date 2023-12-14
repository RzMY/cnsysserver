import tornado.web
from conf.base import BaseHandler,EnterHandler
import datetime
class HeartbeatHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db

    def prepare(self):
        self.cursor = self.db.cursor()

    def on_finish(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()

    def post(self):
        # 更新用户的活跃时间
        username = self.get_current_user()
        if username:
            cursor = self.db.cursor()
            sql = """UPDATE session SET last_active = NOW() WHERE username = %s"""
            print("更新用户{}的活跃时间 当前时间：{}".format(username,datetime.datetime.now()))
            cursor.execute(sql, (username,))
            self.db.commit()