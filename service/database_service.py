#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import os, json
from commons.color import Colors
from utils.database_util import DBUtils
from bean.database import Database
from utils.excel_util import ExcelUtils
from utils.logger_util import LoggerUtil
from utils.dir_util import DirUtil

class DataBaseService:

    config = None
    configPath = './configs/update_by_excel.ini'
    updateByExcelMap = None
    updateByExcelWhereColumns = None
    updateByExcelUpdateColumns = None
    updateByExcelExcelPath = None

    updateByExcelColumnsReadStartRow = None
    updateByExcelColumnsTitle = None
    updateByExcelColumnsReadColumnIndexs = None
    updateByExcelColumnsScannerExcelsDirPath = None
    updateByExcelColumnsScannerExcelSuffix = None
    updateByExcelColumnsWhereColumns = None
    updateByExcelColumnsUpdateColumns = None
    updateByExcelColumnsCustomAppendWhere = None
    updateByExcelColumnsIsCheckNone = True

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(self.configPath, encoding='utf-8')

    def updateByExcel(self):
        '''
        根据Excel表格更新数据库字段
        '''
        self.resetUpdateByExcelConfigInfo()
        self.printDatabaseConfigInfo()
        self.printUpdateByExcelInfo()
        choise = input("是否继续执行[Y/N]：")
        if "Y" == choise.upper():
            pass
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项有误！")
            return

        if not os.path.exists(self.updateByExcelExcelPath):
            Colors.print(Colors.FAIL, "Excel文件不存在！，路径信息：%s"%self.updateByExcelExcelPath)
            return

        if not self.checkExcelAndConfigInfo(): return

        excelData = ExcelUtils.read(self.updateByExcelExcelPath, False)
        logger = LoggerUtil().getLogger('根据Excel表格更新数据库字段')
        connection = DBUtils.getConnection(Database())
        current = 1
        for excelDataItem in excelData:
            updateSql = "UPDATE `%s` SET %s WHERE %s"
            setSql = ""
            whereSql = ""
            for key in excelDataItem.keys():
                dbTableColumnName = self.updateByExcelMap[key]
                # 对数据表格中的值进行类型转换
                value = ""
                if type(excelDataItem[key]) == str:
                    value = '"%s"'%str(excelDataItem[key])
                elif type(excelDataItem[key]) == bool:
                    value = '%s'%bool(excelDataItem[key])
                elif excelDataItem[key] == None:
                    value = "''"
                else:
                    value = excelDataItem[key]

                if dbTableColumnName in self.updateByExcelWhereColumns:
                    whereSql = "%s %s=%s %s "%(whereSql, dbTableColumnName, value, "AND")
                if dbTableColumnName in self.updateByExcelUpdateColumns:
                    setSql = "%s %s=%s %s"%(setSql, dbTableColumnName, value, ",")
            
            updateSql = updateSql%(Database().tableName, setSql.rstrip(","), whereSql.rstrip("AND "))
            logger.info("当前进度 %s / %s, 正在处理SQL：%s"%(current, len(excelData), updateSql))
            DBUtils.update(connection, updateSql)
            current = current + 1
        DBUtils.closeConnect(connection)


    def updateByExcelColumns(self):
        '''
        根据Excel表格列更新数据库字段
        '''
        self.resetUpdateByExcelColumnsConfigInfo()
        self.printDatabaseConfigInfo()
        self.printUpdateByExcelColumnsInfo()
        choise = input("是否继续执行[Y/N]：")
        if "Y" == choise.upper():
            pass
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项有误！")
            return

        if not os.path.exists(self.updateByExcelColumnsScannerExcelsDirPath):
            Colors.print(Colors.FAIL, "路径不存在！，路径信息：%s"%self.updateByExcelColumnsScannerExcelsDirPath)
            return
        if not os.path.isdir(self.updateByExcelColumnsScannerExcelsDirPath):
            Colors.print(Colors.FAIL, "路径不是目录！，路径信息%s"%self.updateByExcelColumnsScannerExcelsDirPath)
            return
        
        excelPaths = DirUtil.filterFilePath(self.updateByExcelColumnsScannerExcelsDirPath, self.updateByExcelColumnsScannerExcelSuffix)
        if len(excelPaths) == 0:
            Colors.print(Colors.FAIL, "没有扫描到后缀名包含 %s 的Excel文件，路径信息%s"%(self.updateByExcelColumnsScannerExcelSuffix, self.updateByExcelColumnsScannerExcelsDirPath))
            return
        else:
            Colors.print(Colors.OKGREEN, "成功扫描到 %s 个表格信息,表格信息如下："%len(excelPaths))
            for excelPath in excelPaths:
                Colors.print(Colors.OKBLUE, excelPath)

        logger = LoggerUtil().getLogger('根据Excel表格更新数据库字段')

        # 存放各个表格的数据内容 key=Excel路径 value=Excel数据
        excelDataMap = {}
        # 存放check后有问题的表格
        errorExcelPaths = []
        for excelPath in excelPaths:
            # 读取并存放单个表格的数据内容
            excelData = ExcelUtils.read(path=excelPath, startRow=self.updateByExcelColumnsReadStartRow, readColumnIndexs=self.updateByExcelColumnsReadColumnIndexs, dataTitle=self.updateByExcelColumnsTitle)
            if self.updateByExcelColumnsIsCheckNone and self.checkExcelNone(excelData):
                errorExcelPaths.append(excelPath)
            excelDataMap[excelPath] = excelData

        if len(errorExcelPaths) > 0:
            for errorExcelPath in errorExcelPaths:
                Colors.print(Colors.FAIL,"Excel: %s 未通过空值校验"%errorExcelPath)
            return

        Colors.print(Colors.OKBLUE, "\n\n成功读取完成 %s 个表格，表格信息入下："%len(excelDataMap.keys()))
        for excelPathKey in excelDataMap.keys():
            Colors.print(Colors.OKBLUE, "%s"%excelPathKey)
        choise = input("是否继续执行[Y/N]：")
        if "Y" == choise.upper():
            pass
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项有误！")
            return
        
        connection = DBUtils.getConnection(Database())
        if connection == None:
            Colors.print(Colors.FAIL,"数据库连接失败，程序结束")
            return

        
        updateSqls = []
        execExcelIndex = 1
        for excelPathKey in excelDataMap.keys():
            execDataIndex = 1
            for excelDataItem in excelDataMap[excelPathKey]:
                updateSql = "UPDATE `%s` SET %s WHERE %s %s;"
                setSql = ""
                whereSql = ""
                for dbTableColumnName in excelDataItem.keys():
                    # 对数据表格中的值进行类型转换
                    value = ""
                    if type(excelDataItem[dbTableColumnName]) == str:
                        value = '"%s"'%str(excelDataItem[dbTableColumnName])
                    elif type(excelDataItem[dbTableColumnName]) == bool:
                        value = '%s'%bool(excelDataItem[dbTableColumnName])
                    elif excelDataItem[dbTableColumnName] == None:
                        value = "''"
                    else:
                        value = excelDataItem[dbTableColumnName]

                    if dbTableColumnName in self.updateByExcelColumnsWhereColumns:
                        whereSql = "%s %s=%s %s "%(whereSql, dbTableColumnName, value, "AND")
                    if dbTableColumnName in self.updateByExcelColumnsUpdateColumns:
                        setSql = "%s %s=%s %s"%(setSql, dbTableColumnName, value, ",")
                
                updateSql = updateSql%(Database().tableName, setSql.rstrip(","), whereSql.rstrip("AND "), self.updateByExcelColumnsCustomAppendWhere)
                updateSqls.append(updateSql)
                logger.info("当前正在生成 %s / %s 个表格数据的 %s / %s 条数据，生成SQL为：%s, 表格路径为：%s"%(execExcelIndex, len(excelDataMap.keys()),execDataIndex, len(excelDataMap[excelPathKey]),updateSql, excelPathKey))
                Colors.print(Colors.OKBLUE, "当前正在生成 %s / %s 个表格数据的 %s / %s 条数据，生成SQL为：%s, 表格路径为：%s"%(execExcelIndex, len(excelDataMap.keys()),execDataIndex, len(excelDataMap[excelPathKey]),updateSql, excelPathKey))
                
                execDataIndex += 1
            execExcelIndex += 1
        
        if len(updateSqls) == 0:
            Colors.print(Colors.FAIL, "\n\n生成SQL数据为 0 条，跳过执行更新操作")
            return
        else:
            Colors.print(Colors.OKGREEN, "\n\n成功生成 %s 条SQL"%(len(updateSqls)))
            for updataSql in updateSqls:
                Colors.print(Colors.OKBLUE, updataSql)

            choise = input("\n是否继续执行[Y/N]：")
            if "Y" == choise.upper():
                DBUtils.batchUpdate(updateSqls)
            elif "N" == choise.upper():
                return
            else:
                Colors.print(Colors.FAIL, "输入选项有误！")
                return

        DBUtils.closeConnect(connection)

    def checkExcelNone(self, excelData):
        '''
        检查表格中是否存在None或空值信息
        Args：
            excelData：数据表格信息
        Return
            存在返回true，不存在返回false
        '''
        for excelDateItem in excelData:
            for key in excelDateItem.keys():
                if excelDateItem[key] == None or len(str(excelDateItem[key])) == 0:
                    return True
        return False

    def checkExcelAndConfigInfo(self):
        '''
        检查配置文件中map与excel表格中的信息是否对应
        '''
        excelTitle = ExcelUtils.read(self.updateByExcelExcelPath, True)
        if not list(self.updateByExcelMap.keys()) == excelTitle:
            Colors.print(Colors.FAIL, "配置文件中的设置与Excel表头不一致，请检查")
            return False
        Colors.print(Colors.OKGREEN, "已通过配置文件中的设置与Excel表头检查校验")
        return True

    def resetUpdateByExcelConfigInfo(self):
        '''
        重新赋值配置文件信息
        '''
        try:
            self.config.read(self.configPath, encoding='utf-8')
            self.updateByExcelMap = json.loads(self.config['update_by_excel']['map'])
            self.updateByExcelWhereColumns = self.config['update_by_excel']['whereColumns'].split()
            self.updateByExcelUpdateColumns = self.config['update_by_excel']['updateColumns'].split()
            self.updateByExcelExcelPath = self.config['update_by_excel']['excelPath']
        except:
            Colors.print(Colors.FAIL, "读取配置文件失败，请检查！")

    def resetUpdateByExcelColumnsConfigInfo(self):
        '''
        重新赋值配置文件信息
        '''
        try:
            self.config.read(self.configPath, encoding='utf-8')
            self.updateByExcelColumnsReadStartRow = int(self.config['update_by_excel_columns']['readStartRow'])
            self.updateByExcelColumnsTitle = self.config['update_by_excel_columns']['title'].split()
            self.updateByExcelColumnsReadColumnIndexs = self.config['update_by_excel_columns']['readColumnIndexs'].split()
            self.updateByExcelColumnsScannerExcelsDirPath = self.config['update_by_excel_columns']['scannerExcelsDirPath']
            self.updateByExcelColumnsWhereColumns = self.config['update_by_excel_columns']['whereColumns'].split()
            self.updateByExcelColumnsUpdateColumns = self.config['update_by_excel_columns']['updateColumns'].split()
            self.updateByExcelColumnsScannerExcelSuffix = self.config['update_by_excel_columns']['scannerExcelSuffix'].split()
            isCheckNone = self.config['update_by_excel_columns']['isCheckNone']
            self.updateByExcelColumnsIsCheckNone = False if isCheckNone.upper() == 'FALSE' else True
            customAppendWhere = self.config['update_by_excel_columns']['customAppendWhere']
            self.updateByExcelColumnsCustomAppendWhere = "" if customAppendWhere == None or len(customAppendWhere) == 0 else customAppendWhere
            # 将字符串数组转换为int数组
            updateByExcelColumnsReadColumnIndexs = []
            for updateByExcelColumnsReadColumnIndex in self.updateByExcelColumnsReadColumnIndexs:
                updateByExcelColumnsReadColumnIndexs.append(int(updateByExcelColumnsReadColumnIndex))
            self.updateByExcelColumnsReadColumnIndexs = updateByExcelColumnsReadColumnIndexs
        except:
            Colors.print(Colors.FAIL, "读取配置文件失败，请检查！")


    def printDatabaseConfigInfo(self):
        Colors.print(Colors.OKBLUE, '''
[数据库连接信息]
连接地址：%s
连接端口：%s
连接数据库名：%s
操作的表名：%s
用户名：%s
密码：%s
'''%(Database().host, Database().port, Database().dbName, Database().tableName, Database().username, Database().password))

    def printUpdateByExcelInfo(self):
        '''
        打印配置文件信息
        '''
        Colors.print(Colors.OKBLUE, '''
[数据库表与Excel表格映射关系]
%s
[数据库表查询的Where条件]
%s
[数据库需要更新的字段列]
%s
[Excel表格所处的路径信息]
%s
'''%(self.updateByExcelMap, self.updateByExcelWhereColumns, self.updateByExcelUpdateColumns, self.updateByExcelExcelPath))

    def printUpdateByExcelColumnsInfo(self):
        '''
        打印配置文件信息
        '''
        Colors.print(Colors.OKBLUE, '''
[Excel表格读取内容的开始行数]
%s
[Excel表格读取内容的列索引]
%s
[数据库字段数组，与读取列成对应关系]
%s
[数据库表查询的Where条件]
%s
[数据库需要更新的字段列]
%s
[数据库更新语句自定义追加的SQL内容]
%s
[是否检查Excel中的空值或None]
%s
[扫描的Excel所在目录路径]
%s
'''%(self.updateByExcelColumnsReadStartRow, self.updateByExcelColumnsReadColumnIndexs, self.updateByExcelColumnsTitle, self.updateByExcelColumnsWhereColumns, self.updateByExcelColumnsUpdateColumns, self.updateByExcelColumnsCustomAppendWhere, self.updateByExcelColumnsIsCheckNone, self.updateByExcelColumnsScannerExcelsDirPath))