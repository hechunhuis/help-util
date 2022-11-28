import os
from commons.color import Colors
from utils.dir_util import DirUtil

class DirService:

    def batchDelete(self):
        '''
        批量删除目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubPath(rootPath)
        self.printScannerPath(subPaths)
        
        
    def batchMove(self):
        '''
        批量移动目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubPath(rootPath)
        self.printScannerPath(subPaths)
        
    def batchCopy(self):
        '''
        批量复制目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubPath(rootPath)
        self.printScannerPath(subPaths)
    
    def batchCreate(self):
        '''
        批量创建目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubPath(rootPath)
        self.printScannerPath(subPaths)

    def getAndCheckDir(self):
        '''
        检查路径
        '''
        while True:
            rootPath = input("请输入将要处理扫描的根目录[N:退出]：")
            if "N" == rootPath.upper() :
                return False
            if not os.path.exists(rootPath):
                Colors.print(Colors.FAIL, "路径不存在！请检查")
            elif not os.path.isdir(rootPath):
                Colors.print(Colors.FAIL, "目标必须为目录")
            else:
                return rootPath
            
    def printScannerPath(self, paths):
        '''
        打印路径
        '''
        Colors.print(Colors.OKGREEN, "成功扫描到 %s 项"%(len(paths)))
        for path in paths:
            Colors.print(Colors.OKBLUE, path)