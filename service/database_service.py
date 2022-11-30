import configparser
import os, json
from commons.color import Colors
from utils.database_util import DBUtils
from bean.database import Database
from utils.excel_util import ExcelUtils
from utils.logger_util import LoggerUtil

class DataBaseService:

    config = None
    configPath = None
    databaseExcelMap = None
    databaseWhereColumns = None
    databaseUpdateColumns = None
    excelPath = None

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.configPath = './configs/update_by_excel.ini'
        self.config.read(self.configPath, encoding='utf-8')

    def updateByExcel(self):
        '''
        根据Excel表格更新数据库字段
        '''
        self.resetConfigInfo()
        self.printConfigInfo()
        choise = input("是否继续执行[Y/N]：")
        if "Y" == choise.upper():
            pass
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项有误！")
            return

        if not os.path.exists(self.excelPath):
            Colors.print(Colors.FAIL, "Excel文件不存在！，路径信息：%s"%self.excelPath)
            return

        if not self.checkExcelAndConfigInfo(): return
        
        

        excelData = ExcelUtils.read(self.excelPath, False)
        logger = LoggerUtil().getLogger('根据Excel表格更新数据库字段')
        connection = DBUtils.getConnection(Database())
        current = 1
        for excelDataItem in excelData:
            updateSql = "UPDATE `%s` SET %s WHERE %s"
            setSql = ""
            whereSql = ""
            for key in excelDataItem.keys():
                dbTableColumnName = self.databaseExcelMap[key]
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

                if dbTableColumnName in self.databaseWhereColumns:
                    whereSql = "%s %s=%s %s "%(whereSql, dbTableColumnName, value, "AND")
                if dbTableColumnName in self.databaseUpdateColumns:
                    setSql = "%s %s=%s %s"%(setSql, dbTableColumnName, value, ",")
            
            updateSql = updateSql%(Database().tableName, setSql.rstrip(","), whereSql.rstrip("AND "))
            logger.info("当前进度 %s / %s, 正在处理SQL：%s"%(current, len(excelData), updateSql))
            DBUtils.update(connection, updateSql)
            current = current + 1
        DBUtils.closeConnect(connection)

    def checkExcelAndConfigInfo(self):
        '''
        检查配置文件中map与excel表格中的信息是否对应
        '''
        excelTitle = ExcelUtils.read(self.excelPath, True)
        if not list(self.databaseExcelMap.keys()) == excelTitle:
            Colors.print(Colors.FAIL, "配置文件中的设置与Excel表头不一致，请检查")
            return False
        Colors.print(Colors.OKGREEN, "已通过配置文件中的设置与Excel表头检查校验")
        return True

    def resetConfigInfo(self):
        '''
        重新赋值配置文件信息
        '''
        try:
            self.databaseExcelMap = json.loads(self.config['database_excel_map']['map'])
            self.databaseWhereColumns = self.config['database_where_columns']['whereColumns'].split()
            self.databaseUpdateColumns = self.config['database_update_columns']['updateColumns'].split()
            self.excelPath = self.config['excel_info']['excelPath']
        except:
            Colors.print(Colors.FAIL, "读取配置文件失败，请检查！")


    def printConfigInfo(self):
        '''
        打印配置文件信息
        '''
        Colors.print(Colors.OKBLUE, '''
请确认配置文件以下信息：
[数据库连接信息]
连接地址：%s
连接端口：%s
连接数据库名：%s
操作的表名：%s
用户名：%s
密码：%s

[数据库表与Excel表格映射关系]
%s

[数据库表查询的Where条件]
%s

[数据库需要更新的字段列]
%s

[Excel表格所处的路径信息]
%s
'''%(Database().host, Database().port, Database().dbName, Database().tableName, Database().username, Database().password, self.databaseExcelMap, self.databaseWhereColumns, self.databaseUpdateColumns, self.excelPath))