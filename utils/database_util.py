'''
    该脚本主要用于连接数据库
'''
import pymysql

class DBUtils:

    host = None
    port = None
    dbName = None
    username = None
    password = None

    def __init__(self, host, port, dbName, username, password) -> None:
        self.host = host
        self.port = port
        self.dbName = dbName
        self.username = username
        self.password = password
    
    @classmethod
    def getConnection(self):
        '''
            设置数据库连接信息
            @retrun connect 返回数据库的连接对象
        '''
        connect = None
        try :
            print("正在进行数据库连接操作：host:%s port:%s dbName:%s username:%s password:%s"%(self.host, self.port, self.dbName, self.username, self.password))
            connect = pymysql.connect(host=self.host,port=self.port, database=self.dbName, user=self.username, password=self.password)
        except Exception as e :
            print("数据库连接失败！\n%s"%e)
        print("数据库连接成功")
        return connect

    @classmethod
    def closeConnect(self, connect):
        '''
            关闭数据库连接
            @param connect 数据库连接对象
        '''
        try:
            connect.close()
            print("数据库连接关闭成功")
        except Exception as e:
            print("数据库连接关闭失败！")

    @classmethod
    def fetch(self, connect, sql:str):
        '''
            查询单条信息
            @param connect 数据库连接对象
            @param sql str 查询语句
        '''
        cur = connect.cursor(cursor=pymysql.cursors.DictCursor)
        print("开始执行SQL：%s"%sql)
        cur.execute(sql)
        data = cur.fetchone()
        print("查询到 %s 条符合条件的记录，信息：%s"%(len(data), data))
        return data

    @classmethod
    def query(self, connect, sql:str):
        '''
            查询多条信息
            @param connect 数据库连接对象
            @param sql str 查询语句
        '''
        cur = connect.cursor(cursor=pymysql.cursors.DictCursor)
        print("开始执行SQL：%s"%sql)
        cur.execute(sql)
        data = cur.fetchall()
        print("查询到 %s 条符合条件的记录，信息：%s"%(len(data), data))
        return data