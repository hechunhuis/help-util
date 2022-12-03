#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    该脚本主要用于连接数据库
'''
import pymysql
from commons.color import Colors
from bean.database import Database
from utils.logger_util import LoggerUtil
from commons.my_thread import MyThread
from concurrent.futures import ThreadPoolExecutor
import time
class DBUtils:

    logger = LoggerUtil().getLogger('DB执行记录')

    @classmethod
    def getConnection(self, database):
        '''
            设置数据库连接信息
            @retrun connect 返回数据库的连接对象
        '''
        connect = None
        for index in range(1,6):
            try :
                Colors.print(Colors.OKBLUE, "正在进行第 %s 次数据库连接操作：%s"%(index, database.toString()))
                connect = pymysql.connect(host=database.host, port=database.port, database=database.dbName, user=database.username, password=database.password)
                if not connect == None:
                    Colors.print(Colors.OKGREEN, "数据库连接成功")
                    return connect
            except Exception as e :
                connectTimeTnterval = 5
                Colors.print(Colors.FAIL, "数据库连接失败， %s 秒后进行重新连接尝试！\n%s"%(connectTimeTnterval, e))
                time.sleep(connectTimeTnterval)
        Colors.print(Colors.FAIL, "数据库连接失败，请稍后再试")
            
        

    @classmethod
    def closeConnect(self, connect):
        '''
            关闭数据库连接
            @param connect 数据库连接对象
        '''
        try:
            connect.close()
            self.logger.info("数据库连接关闭成功")
            Colors.print(Colors.OKGREEN, "数据库连接关闭成功")
        except Exception as e:
            self.logger.error("数据库连接关闭失败！")
            Colors.print(Colors.FAIL, "数据库连接关闭失败！")

    @classmethod
    def fetch(self, connect, sql:str):
        '''
            查询单条信息
            @param connect 数据库连接对象
            @param sql str 查询语句
        '''
        if connect == None:
            connect = self.getConnection(Database())
        cur = connect.cursor(cursor=pymysql.cursors.DictCursor)
        self.logger.info("开始执行SQL：%s"%sql)
        Colors.print(Colors.OKBLUE, "开始执行SQL：%s"%sql)
        cur.execute(sql)
        data = cur.fetchone()
        self.logger.info("查询到 %s 条符合条件的记录，信息：%s"%(len(data), data))
        Colors.print(Colors.OKBLUE, "查询到 %s 条符合条件的记录，信息：%s"%(len(data), data))
        return data

    @classmethod
    def query(self, connect, sql:str):
        '''
            查询多条信息
            @param connect 数据库连接对象
            @param sql str 查询语句
        '''
        if connect == None:
            connect = self.getConnection(Database())
        cur = connect.cursor(cursor=pymysql.cursors.DictCursor)
        self.logger.info("开始执行SQL：%s"%sql)
        Colors.print(Colors.OKBLUE, "开始执行SQL：%s"%sql)
        cur.execute(sql)
        data = cur.fetchall()
        self.logger.info("查询到 %s 条符合条件的记录，信息：%s"%(len(data), data))
        Colors.print(Colors.OKBLUE, "查询到 %s 条符合条件的记录，信息：%s"%(len(data), data))
        return data

    @classmethod
    def update(self, connect, sql:str):
        '''
            更新数据库操作
        '''
        result = {}
        result['code']='fail'
        result['info']=sql
        if connect == None:
            connect = self.getConnection(Database())
        try:
            cursor = connect.cursor()
            self.logger.info("开始执行SQL：%s"%sql)
            Colors.print(Colors.OKBLUE, "开始执行SQL：%s"%sql)
            cursor.execute(sql)
            connect.commit()
            self.logger.info("提交事务成功")
            Colors.print(Colors.OKGREEN, "提交事务成功")
            result['code'] = 'success'
        except Exception as e:
            print(e)
            self.logger.error("执行SQL：%s 失败！开始事务回滚"%sql)
            Colors.print(Colors.FAIL, "执行SQL：%s 失败！开始事务回滚"%sql)
            connect.rollback()
            Colors.print(Colors.OKGREEN, "事务回滚完成")
        self.closeConnect(connect)
        return result

    @classmethod
    def batchUpdate(self, sqls):
        '''
        多线程批量更新SQL
        '''
        
        successRecord = []
        failedRecord = []
        execIndex = 1
        
        for sql in sqls:
            Colors.print(Colors.OKCYAN, "正在执行 %s / %s 条SQL"%(execIndex, len(sqls)))
            result = self.update(None, sql)
            if result['code'] == 'success':
                successRecord.append(result['info'])
            else:
                failedRecord.append(result['info'])
            execIndex += 1
        
        Colors.print(Colors.OKGREEN, "总共处理完 %s 个语句："%(len(successRecord) + len(failedRecord)))
        Colors.print(Colors.OKGREEN, "成功处理了 %s / %s个语句：语句如下："%(len(successRecord), len(successRecord) + len(failedRecord)))
        for success in successRecord:
            Colors.print(Colors.OKGREEN, success)
        Colors.print(Colors.FAIL, "其中 %s / %s 个语句处理失败：语句如下："%(len(failedRecord), len(successRecord) + len(failedRecord))) 
        for failed in failedRecord:
            Colors.print(Colors.FAIL, failed)
