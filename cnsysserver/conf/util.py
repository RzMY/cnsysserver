# 工具模块，提供所需要的公共方法
import hashlib

class UtilTools():
    def md5(btext):
        m = hashlib.md5()
        m.update(btext.encode())
        return m.hexdigest()