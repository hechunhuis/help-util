'''
    导出表格工具类
'''
import openpyxl
from logger_util import LoggerUtil

class ExcelUtils:
    
    @classmethod
    def save(self, path:str, sheet:str, data):
        '''
            保存为Excel表格
            Args:
                path:表格生成路径
                sheet:要创建的sheet页名称
                data:要导出的数据对象,示例数据：
                [\n
                    ['title1','title2','title3',……],\n
                    ['data1' ,'data2' ,'data3' ,……],\n
                    …………\n
                ]
            Returns:
                path:
        '''
        workBook = openpyxl.Workbook()
        sheetTable = workBook.create_sheet(sheet)
        for rowIndex in range(len(data)):
            print("导出Excel：正在处理 %s / %s 条数据"%(rowIndex+1, len(data)))
            for columnIndex in range(len(data[rowIndex])) :
                sheetTable.cell(row=rowIndex+1, column=columnIndex+1, value=data[rowIndex][columnIndex])
        workBook.save(path)
        print("成功导出Excel数据，路径：%s，sheet页为：%s"%(path, sheet))
