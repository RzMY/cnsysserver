# 后台的控制模块和业务模块
import tornado.web
from conf.base import BaseHandler,EnterHandler

class MainHandler(BaseHandler):
    def initialize(self, db):
        # 初始化成员方法
        self.db = db

    def prepare(self):
        self.cursor = self.db.cursor()

    def on_finish(self):
        self.cursor.close()

    @tornado.web.authenticated
    def get(self):
        # 先处理数据

        # 获取用户信息
        kwages = dict()
        kwages["username"] = BaseHandler.get_current_user(self)

        # 查询用户头像
        sql = """SELECT avatar_url FROM user_info WHERE username = %s"""
        self.cursor.execute(sql, (kwages["username"],))
        avatar_url = self.cursor.fetchone()
        kwages["avatar_url"] = avatar_url[0]
        
        # 获取复购率
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
        fugou = self.cursor.fetchall()
        
        # 获取回购率
        sql_huigou = \
            """
            SELECT DATE_FORMAT(m1,'%Y-%m'),COUNT(m1),COUNT(m2),COUNT(m2)/COUNT(m1) FROM
            (SELECT CUSTOMERID,DATE_FORMAT(INVOICEDATE,'%Y-%m-01') as m1 FROM OnlineRetail 
            GROUP BY DATE_FORMAT(INVOICEDATE,'%Y-%m-01'),customerid) A 
            LEFT JOIN
            (SELECT CUSTOMERID,DATE_FORMAT(INVOICEDATE,'%Y-%m-01') as m2 FROM OnlineRetail 
            GROUP BY DATE_FORMAT(INVOICEDATE,'%Y-%m-01'),customerid) B 
            ON A.CUSTOMERID = B.CUSTOMERID
            AND m1 = DATE_SUB(m2,INTERVAL 1 MONTH)
            GROUP BY m1;
            """
        self.cursor.execute(sql_huigou)
        huigou = self.cursor.fetchall()

        # 获取头部贡献率
        
        # 获取低质量客户贡献度
        sql_diduan = \
            """
            SELECT SUM(SALES)/9769872 AS '消费占比',
            COUNT(us)/4372 AS '用户占比',
            SUM(SALES)/COUNT(us) AS '客单价' FROM
            (SELECT CUSTOMERID AS us,ROUND(SUM(UNITPRICE * QUANTITY),2) AS SALES
            FROM OnlineRetail WHERE CustomerID IS NOT NULL
            AND QUANTITY>0
            GROUP BY CUSTOMERID 
            ORDER BY SUM(UNITPRICE * QUANTITY) LIMIT 3000) T1;
            """
        self.cursor.execute(sql_diduan)
        diduan = self.cursor.fetchall()
        
        # 获取高质量客户贡献度
        sql_gaoduan = \
            """
            SELECT 
            SUM(SALES)/9769872 AS '消费占比',
            COUNT(us)/4372 AS '用户占比',
            SUM(SALES)/COUNT(us) AS '客单价' FROM
            (SELECT CUSTOMERID AS us,ROUND(SUM(UNITPRICE * QUANTITY),2) AS SALES
            FROM OnlineRetail WHERE CustomerID IS NOT NULL 
            GROUP BY CUSTOMERID 
            ORDER BY SUM(UNITPRICE * QUANTITY) DESC LIMIT 874) T1;
            """
        self.cursor.execute(sql_gaoduan)
        gaoduan = self.cursor.fetchall()
        
        # 获取每月消费情况
        
        sql_xiaofei = \
            """    
            SELECT 
            YEAR(InvoiceDate) AS Year,
            MONTH(InvoiceDate) AS Month,
            COUNT(DISTINCT CustomerID) AS '消费人数',
            SUM(Quantity * UnitPrice) AS '消费金额'
            FROM 
                OnlineRetail 
            GROUP BY 
                YEAR(InvoiceDate), MONTH(InvoiceDate)
            ORDER BY 
                Year, Month;
            """
        self.cursor.execute(sql_xiaofei)
        xiaofei = self.cursor.fetchall()
        
        # 获取购买周期情况
        
        sql_zhouqi = \
            """
            SELECT CustomerID, AVG(gap) as 平均购买周期 FROM(
            select CustomerID,time1,time2 ,datediff(time1,time2) AS gap 
            from(
            select
            CustomerID,
            InvoiceNo,
            InvoiceDate as time1,
            LAG(InvoiceDate,1) OVER(PARTITION BY CustomerID) AS time2
            from OnlineRetail 
            WHERE CustomerID is not NULL
            GROUP BY InvoiceNo,CustomerID,InvoiceDate)a)b
            GROUP BY CustomerID HAVING AVG(gap) >0;
            """
        self.cursor.execute(sql_zhouqi)
        zhouqi = self.cursor.fetchall()
        
        # 获取平局购买周期
        
        sql_pingjunzhouqi = \
            """
            SELECT AVG(gap) as 总平均购买周期 FROM(
            select CustomerID,time1,rank1,time2 ,datediff(time1,time2) AS gap 
            from(
            select
            CustomerID,
            InvoiceNo,
            InvoiceDate as time1,
            ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY InvoiceDate) AS rank1,
            LAG(InvoiceDate,1) OVER(PARTITION BY CustomerID ORDER BY InvoiceDate) AS time2
            from OnlineRetail 
            WHERE CustomerID is not NULL
            GROUP BY InvoiceNo,CustomerID,InvoiceDate)a)b;
            """
        self.cursor.execute(sql_pingjunzhouqi)
        pingjunzhouqi = self.cursor.fetchall()
        
        self.render("main.html", fugou = fugou, huigou = huigou, diduan = diduan, gaoduan = gaoduan, xiaofei = xiaofei, zhouqi = zhouqi, pingjunzhouqi = pingjunzhouqi, **kwages)