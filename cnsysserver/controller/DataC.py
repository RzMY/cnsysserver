# 公共后台数据请求模块
import tornado.web
from conf.base import BaseHandler,EnterHandler
import json
class DataHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db
        
    def prepare(self):
        self.cursor = self.db.cursor()
        
    def on_finish(self):
        self.cursor.close()
        
    @tornado.web.authenticated
    def get(self):
        m = self.get_argument("m","fugou")
        if m == "fugou":
            # 先处理数据
            sql_fugou = \
"""
SELECT
	yr,
	mt,
	COUNT(
	IF
		(
			t1.orders > 1,
			t1.orders,
		NULL 
		) 
	) AS a,
	COUNT( t1.orders ) AS b, COUNT(
	IF
		(
			t1.orders > 1,
			t1.orders,
		NULL 
		) 
	) / COUNT( t1.orders )
FROM
	(
	SELECT YEAR
		( InvoiceDate ) AS yr,
		MONTH ( InvoiceDate ) AS mt,
		CustomerId,
		COUNT( DISTINCT InvoiceNo ) AS orders 
	FROM
		OnlineRetail 
	GROUP BY
		YEAR ( InvoiceDate ),
		MONTH ( InvoiceDate ),
		CustomerId 
	) AS t1 
GROUP BY
	yr,
	mt
 """
            self.cursor.execute(sql_fugou)
            resinfo = self.cursor.fetchall()
            # 需要讲数据转换后返回给页面-ajax
        elif m == "total":
            self.write("总数据")