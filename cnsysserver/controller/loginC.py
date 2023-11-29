from conf.base import BaseHandler,EnterHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.write("默认登陆页")
        self.set_header("Content-Type","text/html")
        self.render("login.html")
        
    def post(self):
        uName = self.get_argument("userName", default = '', strip=True)
        uPass = self.get_argument("userPass", default = '', strip=True)
        print("用户名：{}，密码：{}".format(uName,uPass))
        # 处理请求到后台的数据
        # 登陆业务
        # 配合SQL语句，查询数据库
        # DDL 数据库定义语言 库database 表table 字段field 新建create 删除drop 修改alter
        # DML 数据库管理语言 新增insert 删除delete 修改update
        # DQL 数据库查询语言 查询select
        
        if not all((uName, uPass)):
            self.write('{"msg"}')