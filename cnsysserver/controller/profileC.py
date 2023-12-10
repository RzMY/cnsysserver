# 个人信息维护
import tornado.web
import os
from conf.base import BaseHandler,EnterHandler

class ProfileHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db

    def prepare(self):
        self.cursor = self.db.cursor()

    def on_finish(self):
        self.cursor.close()

    @tornado.web.authenticated
    def get(self):

        kwages = dict()
        kwages["username"] = BaseHandler.get_current_user(self)

        # 查询用户头像
        sql = """SELECT * FROM user_info WHERE username = %s"""
        # (1, 'user1', '7c6a180b36896a0a8c02787eeafb0e4c', '张三', 25, '13800138000', '../static/images/cat_default_avatar.jpg')
        self.cursor.execute(sql, (kwages["username"],))
        info = self.cursor.fetchone()
        kwages["key"] = info[0]
        kwages["username"] = info[1]
        kwages["realname"] = info[3]
        kwages["age"] = info[4]
        kwages["phone"] = info[5]
        kwages["avatar_url"] = info[6]
        
        self.render("profile.html", **kwages)
        
    def post(self):
        kwages = dict()
        kwages["username"] = BaseHandler.get_current_user(self)

        # 查询用户头像
        sql = """SELECT * FROM user_info WHERE username = %s"""
        # (1, 'user1', '7c6a180b36896a0a8c02787eeafb0e4c', '张三', 25, '13800138000', '../static/images/cat_default_avatar.jpg')
        self.cursor.execute(sql, (kwages["username"],))
        info = self.cursor.fetchone()
        print(info)
        kwages["username"] = info[1]
        kwages["realname"] = info[3]
        kwages["age"] = info[4]
        kwages["phone"] = info[5]
        
        # 将前台数据更新到数据库
        uRealName = self.get_argument("realName", default = kwages['realname'], strip=True)
        uAge = self.get_argument("age", default = kwages['age'], strip=True)
        uPhone = self.get_argument("phone", default = kwages['phone'], strip=True)
        
        # 处理上传的头像文件
        avatar = self.request.files.get('avatar')
        if avatar:
            avatar = avatar[0]
            # 获取原始文件的扩展名
            _, ext = os.path.splitext(avatar['filename'])
            # 生成新的文件名
            avatar_filename = 'avatar_' + kwages["username"] + ext
            avatar_path = os.path.join('static/images', avatar_filename)
            with open(avatar_path, 'wb') as f:
                f.write(avatar['body'])
            # 更新头像URL
            avatar_url = '../' + avatar_path
        else:
            avatar_url = info[6]  # 使用旧的头像URL
        sql = \
            """
            UPDATE user_info
            SET real_name = %s, age = %s, phone_number = %s, avatar_url = %s
            WHERE username = %s
            """
        if uRealName == "":
            uRealName = kwages['realname']
        if uAge == "":
            uAge = kwages['age']
        if uPhone == "":
            uPhone = kwages['phone']
            
        affected_rows = self.cursor.execute(sql, (uRealName, uAge, uPhone, avatar_url, kwages["username"]))
        if affected_rows > 0:
            self.db.commit()
            self.write('{"msg":true}')
        else:
            self.write('{"msg":false}')
        