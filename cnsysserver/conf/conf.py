# 定义视图及程序的核心基础配置，包括是否开启debug，增加安全框架，约定静态资源的路径，约定默认页面
import os
import pymysql

# 定义视图层
setting = dict(
    dubug = True,# 允许开发阶段热部署
    xsrf_cookies = True,# 避免黑客利用跨站脚本获得用户信息
    compress_response = True,# 压缩响应信息
    static_path = os.path.join(os.getcwd(),"static"),# 配置静态资源路径
    template_path = os.path.join(os.getcwd(),"templates"),# 配置模板路径
    cookie_secret = "123456",# 配置cookie加密密钥
    static_url_prefix = "/static/",# 配置静态资源访问路径: http://localhost:10086/static/...
    login_url = "/login",# 配置默认登录页面
    static_handler_args = dict(default_filename = "index.html"),# 配置默认访问页面
)

# 全局的数据库操作对象
db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "qwertyuiop0!",
    db = "cnosdb",
    autocommit = True
)