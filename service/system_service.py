from commons.color import Colors
from model.menu_model import MenuModel
from service.uuid_service import UUIDService
from service.date_service import DateService
from service.dir_service import DirService

import os
import sys

class SystemService:
    '''
    系统服务类
    如果您想自定义菜单，只需要重新构建menus数据即可，menus数组包含MenuModel对象列表
    MenuModel:
        id(主键),parentId(父主键),name(功能菜单名称),description(功能菜单描述),method(功能菜单所对应执行的方法)
    '''

    logoPath = "logo.ini"
    menus = []
    currentMenuPath = []

    def __init__(self) -> None:
        '''
        初始化菜单信息
        '''
        self.menus.append(MenuModel(1, 0, "目录工具", "", None))

        self.menus.append(MenuModel(2, 1, "批量删除目录", "【根据规则批量删除目录】", DirService().batchDelete))
        self.menus.append(MenuModel(3, 1, "批量移动目录", "【根据规则批量移动目录】", DirService().batchMove))
        self.menus.append(MenuModel(4, 1, "批量复制目录", "【根据规则批量复制目录】", DirService().batchCopy))
        self.menus.append(MenuModel(5, 1, "批量创建目录", "【根据规则批量创建目录】", DirService().batchCreate))

        self.menus.append(MenuModel(6, 0, "UUID工具", "", None))
        self.menus.append(MenuModel(7, 6, "基于时间戳生成", "【随机生成UUID】", UUIDService().getUUIDByTime))
        self.menus.append(MenuModel(8, 6, "基于随机数生成", "【随机生成UUID】", UUIDService().getUUIDByRan))
        self.menus.append(MenuModel(9, 6, "基于名字和MD5散列值生成", "【随机生成UUID】", UUIDService().getUUIDBySpec))
        self.menus.append(MenuModel(10, 6, "基于名字和SAHI值生成", "【随机生成UUID】", UUIDService().getUUIDBySha))

        self.menus.append(MenuModel(11, 0, "时间工具", "", None))
        self.menus.append(MenuModel(12, 11, "将时间戳转换为日期格式", "", DateService().converTimeToDate))
        self.menus.append(MenuModel(13, 11, "将日期转换为时间戳", "", DateService().converDateToTime))
        
        self.menus.append(MenuModel(14, 0, "数据库工具", "", None))
        self.menus.append(MenuModel(15, 14, "批量设置数据库字段值", "【根据表格对应关系批量设置】", None))

        self.menus.append(MenuModel(0, 0, "退出", "", sys.exit))
    
    def printLogo(self):
        '''
            打印logo信息
        '''
        myfile = open(self.logoPath, encoding="utf-8")
        line = myfile.readline()
        print("\n")
        while line:    
            current_line = line.strip()
            Colors.print(Colors.OKBLUE, current_line)
            line = myfile.readline()
        print("\n")
        myfile.close()
        pass

    def getById(self, id):
        '''
        根据ID获取menu对象
        '''
        for menu in self.menus:
            if menu.id == id:
                return menu
            
    def getMenuByParentId(self, id):
        '''
        根据父ID获取子菜单信息
        '''
        subMenus = []
        for menu in self.menus:
            if menu.parentId == id:
                subMenus.append(menu)
        return subMenus
    
    def checkSelect(self, parentId, selected):
        '''
        检查子菜单中是否包含用户输入选项
        '''
        if(not selected.isdigit()):
            Colors.print(Colors.FAIL, "请输入合法选项！")
            return False
        selected = int(selected)
        for meun in self.getMenuByParentId(parentId) :
            if meun.id == selected:
                return True
        Colors.print(Colors.FAIL, "请输入合法选项！")
        return False
     
    def menuController(self, id=0):
        '''
        获取菜单控制信息
        '''
        self.currentMenuPath = []
        while True:
            subMenus = self.getMenuByParentId(id)
            if len(subMenus) > 0:
                self.printLogo()
                self.printCurrentMenuPath()
                for menu in subMenus:
                    consoleId = menu.id if (menu.id > 10) else "%s%s"%(menu.id, " ")
                    Colors.print(Colors.OKGREEN, "%s. %s%s"%(consoleId, menu.name, menu.description))
                while True:
                    selected = input("\n请选择菜单选项[回车返回上级]：")
                    if selected == '':
                        self.currentMenuPath.remove(self.getById(id).name)
                        id = self.getById(id).parentId
                        break
                    if self.checkSelect(id, selected):
                        id = int(selected)
                        if id == 0:
                            return id
                        self.currentMenuPath.append(self.getById(id).name)
                        break
                os.system('cls || clear')
            else:
                self.printLogo()
                return id
            
    def runMethod(self, id):
        '''
        运行选项对应的方法
        '''
        for menu in self.menus:
            if menu.id == id:
                if menu.method == None:
                    Colors.print(Colors.FAIL, "功能暂未开放！")
                else:
                    menu.method()
                break
    
    def printCurrentMenuPath(self):
        absoluteMenuPath = "当前菜单路径：根路径"
        for currentMenu in self.currentMenuPath:
            absoluteMenuPath = absoluteMenuPath + "/" + currentMenu
        Colors.print(Colors.OKBLUE, absoluteMenuPath + "\n")
if __name__ == "__main__":
    # 运行示例
    # SystemService.runMethod(SystemService.menuController())
    pass