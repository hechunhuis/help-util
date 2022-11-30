#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from commons.color import Colors
import datetime, time

class DateService:

    def converDateToTime(self):
        '''
        将日期转换为时间戳
        '''
        date = input("请输入日期(yyyy-MM-dd HH:mm:ss):")
        try:
            timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            Colors.print(Colors.OKGREEN, timeStamp)
        except:
            Colors.print(Colors.FAIL, "日期格式错误！")
        finally:
            return

    def converTimeToDate(self):
        '''
        将时间戳转换为日期
        '''
        timeStamp = input("请输入时间戳：")
        
        if len(timeStamp) == 13 :
            timeStamp = timeStamp / 1000
        elif len(timeStamp) == 10 :
            pass
        try:
            timeStamp = int(timeStamp)
            time_local = time.localtime(timeStamp)
            Colors.print(Colors.OKGREEN, time.strftime("%Y-%m-%d %H:%M:%S", time_local))
        except:
            Colors.print(Colors.FAIL, "时间戳格式错误！")
        finally:
            return