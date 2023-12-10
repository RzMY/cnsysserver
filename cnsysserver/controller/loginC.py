from conf.base import BaseHandler,EnterHandler
import time
from conf.util import UtilTools

class LoginHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db
        
    def prepare(self):
        self.cursor = self.db.cursor()
        
    def on_finish(self):
        self.cursor.close()
        
    def get(self):
        # self.write("默认登陆页")
        self.set_header("Content-Type","text/html")
        self.render("login.html")
                
    def post(self):
        post_type = self.get_argument("type", default = '', strip=True)
        if post_type == "sign_in":
            uName = self.get_argument("userName", default = '', strip=True)
            uPass = self.get_argument("passWord", default = '', strip=True)
            print("用户名：{}，密码：{} 尝试登录".format(uName,uPass))
            uPass = UtilTools.md5(uPass)
            # print("用户名：{}，密码：{}".format(uName,uPass))
            # 处理请求到后台的数据
            # 登陆业务
            # 配合SQL语句，查询数据库
            # DDL 数据库定义语言 库database 表table 字段field 新建create 删除drop 修改alter
            # DML 数据库管理语言 新增insert 删除delete 修改update
            # DQL 数据库查询语言 查询select
            
            sql = """select * from user_info where username = %s and password = %s"""
            if not all((uName,uPass)):
                # 前后一致性验证
                self.write('{"msg":false}')
            else:
                # 将SQL语句发送到数据库执行
                self.cursor.execute(sql,(uName,uPass))
                resinfo = self.cursor.fetchall()
                # resinfo 放置的是查询到的数据
                # print(resinfo)
                if len(resinfo) == 1:
                    # 用户名和密码正确
                    self.set_secure_cookie("userName",uName,expires = time.time() + 6 * 60 * 24)
                    self.write('{"msg":true}')
                else:
                    self.write('{"msg":false}')
        elif post_type == "sign_up":
            uName = self.get_argument("userName", default = '', strip=True)
            uPass = self.get_argument("passWord", default = '', strip=True)
            uRealName = self.get_argument("realName", default = '', strip=True)
            uAge = self.get_argument("age", default = '', strip=True)
            uPhone = self.get_argument("phone", default = '', strip=True)
            
            print("用户名：{}，密码：{} 尝试注册".format(uName,uPass))
            uPass = UtilTools.md5(uPass)
            
            sql = """insert into user_info(username,password,real_name,age,phone_number) values(%s,%s,%s,%s,%s)"""
            
            if not all((uName,uPass,uRealName,uAge,uPhone)):
                # 前后一致性验证
                self.write('{"msg":false}')
            else:
                affected_rows = self.cursor.execute(sql,(uName,uPass,uRealName,uAge,uPhone))
                if affected_rows > 0:
                    self.db.commit()
                    self.write('{"msg":true}')
                else:
                    self.write('{"msg":false}')