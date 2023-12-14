from conf.base import BaseHandler,EnterHandler
import time
from conf.util import UtilTools
import uuid

class LoginHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db
        
    def prepare(self):
        self.cursor = self.db.cursor()
        self.session_id = self.get_secure_cookie("session_id")
        if not self.session_id:
            self.session_id = self.create_session_id()
            self.set_secure_cookie("session_id", self.session_id)
        
    def create_session_id(self):
        # 使用uuid4来生成一个随机的UUID
        session_id = str(uuid.uuid4())
        return session_id
    
    def on_finish(self):
        self.cursor.close()
        
    def get(self):
        # self.write("默认登陆页")
        self.set_header("Content-Type","text/html")
        self.render("login.html")
                
    def post(self):
        post_type = self.get_argument("type", default = '', strip=True)
        if post_type == "sign_in":
            uTel = self.get_argument("phoneNumber", default = '', strip=True)
            uPass = self.get_argument("passWord", default = '', strip=True)
            print("手机号：{}，密码：{} 尝试登录".format(uTel,uPass))
            uPass = UtilTools.md5(uPass)
            # print("用户名：{}，密码：{}".format(uName,uPass))
            # 处理请求到后台的数据
            # 登陆业务
            # 配合SQL语句，查询数据库
            # DDL 数据库定义语言 库database 表table 字段field 新建create 删除drop 修改alter
            # DML 数据库管理语言 新增insert 删除delete 修改update
            # DQL 数据库查询语言 查询select
            
            sql = """select * from user_info where phone_number = %s and password = %s"""
            if not all((uTel,uPass)):
                # 前后一致性验证
                self.write('{"msg":false}')
            else:
                # 将SQL语句发送到数据库执行
                self.cursor.execute(sql,(uTel,uPass))
                resinfo = self.cursor.fetchall()
                # resinfo 放置的是查询到的数据
                # print(resinfo)
                if len(resinfo) == 1:
                    # 查询用户的username
                    sql = """SELECT username FROM user_info WHERE phone_number = %s"""
                    self.cursor.execute(sql, (uTel,))
                    userame = self.cursor.fetchone()
                    uName = userame[0]
                    # 用户名和密码正确
                    self.set_secure_cookie("userName",uName,expires = time.time() + 6 * 60 * 24)
                    
                    # 查询数据库中的session_id
                    sql = """SELECT session_id FROM session WHERE username = %s"""
                    self.cursor.execute(sql, (uName,))
                    session_data = self.cursor.fetchone()
                    if session_data[0] == None:
                        # 如果数据库中没有session_id，则插入一个
                        sql = """UPDATE session SET session_id = %s WHERE username = %s"""
                        self.cursor.execute(sql, (self.session_id, uName))
                        self.db.commit()
                        self.write('{"msg":true}')
                    elif session_data[0] != self.session_id:
                        # 说明用户已经在其他地方登陆
                        self.clear_cookie("session_id")
                        self.clear_cookie("userName")
                        self.write('{"msg":"another"}')
                else:
                    self.write('{"msg":false}')
        elif post_type == "sign_up":
            uName = self.get_argument("userName", default = '', strip=True)
            uPass = self.get_argument("passWord", default = '', strip=True)
            uRealName = self.get_argument("realName", default = '', strip=True)
            uAge = self.get_argument("age", default = '', strip=True)
            uPhone = self.get_argument("phone", default = '', strip=True)
            
            print("手机号：{}，密码：{} 尝试注册".format(uPhone,uPass))
            uPass = UtilTools.md5(uPass)
            
            # 查询数据库中是否已经存在该用户
            sql = """select * from user_info where username = %s or phone_number = %s"""
            self.cursor.execute(sql,(uName,uPhone))
            resinfo = self.cursor.fetchall()
            if len(resinfo) > 0:
                # 说明该用户已经存在
                self.write('{"msg":"exist"}')
            else:
                # 说明该用户不存在
                # 将用户信息插入到数据库
                sql = """insert into user_info(username,password,real_name,age,phone_number) values(%s,%s,%s,%s,%s)"""
                sql_session = """INSERT INTO session (username, session_id) VALUES (%s, %s)"""
                if not all((uName,uPass,uRealName,uAge,uPhone)):
                    # 前后一致性验证
                    self.write('{"msg":false}')
                else:
                    self.cursor.execute(sql_session, (uName, ''))
                    self.db.commit()
                    affected_rows = self.cursor.execute(sql,(uName,uPass,uRealName,uAge,uPhone))
                    if affected_rows > 0:
                        self.db.commit()
                        self.write('{"msg":true}')
                    else:
                        self.write('{"msg":false}')