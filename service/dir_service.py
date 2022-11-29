import os
from commons.color import Colors
from utils.dir_util import DirUtil
from utils.logger_util import LoggerUtil

class DirService:

    def batchDelete(self):
        '''
        批量删除目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
        self.printScannerPath(subPaths)
        
        
    def batchMove(self):
        '''
        批量移动目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
        self.printScannerPath(subPaths)
        
    def batchCopy(self):
        '''
        批量复制目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
        self.printScannerPath(subPaths)
    
    def batchCreate(self):
        '''
        批量创建目录
        '''
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
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

    def batchPreAppendName(self):
        '''
        批量前追加目录文件名称
        '''
        
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
        dirNames = DirUtil.filteDirPath(rootPath, subPaths)
        if len(dirNames) == 0:
            Colors.print(Colors.FAIL, "扫描到子目录为空！")
            return
        preName = input("请输入前追加的名称：")
        Colors.print(Colors.OKBLUE, "将对 %s 下的目录名进行前追加操作，追加内容为：%s，预计处理目录共 %s 条，目录信息如下，请确认"%(rootPath, preName, len(dirNames)))
        for dirPath in dirNames:
            Colors.print(Colors.OKBLUE, os.path.join(rootPath, dirPath))
        choise = input("是否继续执行操作[Y/N]：")
        if "Y" == choise.upper():
            logger = LoggerUtil().getLogger('目录操作-批量目录名前追加字段')
            for dirPath in dirNames:
                oldName = os.path.join(rootPath, dirPath)
                newName = os.path.join(rootPath, '%s%s'%(preName, dirPath))
                os.rename(oldName, newName)
                logger.info("成功将 %s 重命名为 %s"%(oldName, newName))
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项不合法！")
            return
        

    def batchPostAppendName(self):
        '''
        批量后追加目录文件名称
        '''
        
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
        dirNames = DirUtil.filteDirPath(rootPath, subPaths)
        if len(dirNames) == 0:
            Colors.print(Colors.FAIL, "扫描到子目录为空！")
            return
        postName = input("请输入后追加的名称：")
        Colors.print(Colors.OKBLUE, "将对 %s 下的目录名进行后追加操作，追加内容为：%s，预计处理目录共 %s 条，目录信息如下，请确认"%(rootPath, postName, len(dirNames)))
        for dirPath in dirNames:
            Colors.print(Colors.OKBLUE, os.path.join(rootPath, dirPath))
        choise = input("是否继续执行操作[Y/N]：")
        if "Y" == choise.upper():
            logger = LoggerUtil().getLogger('目录操作-批量目录名后追加字段')
            for dirPath in dirNames:
                oldName = os.path.join(rootPath, dirPath)
                newName = os.path.join(rootPath, '%s%s'%(dirPath, postName))
                os.rename(oldName, newName)
                logger.info("成功将 %s 重命名为 %s"%(oldName, newName))
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项不合法！")
            return

    def batchRepalceAppendName(self):
        '''
        批量前追加目录文件名称
        '''
        
        rootPath = self.getAndCheckDir()
        if not rootPath:
            return
        subPaths = DirUtil.getSubName(rootPath)
        dirNames = DirUtil.filteDirPath(rootPath, subPaths)
        if len(dirNames) == 0:
            Colors.print(Colors.FAIL, "扫描到子目录为空！")
            return
        
        sourceName = input("请输入目录中存在的字符/字符串：")
        targetName = input("请输入目标的字符/字符串：")
        Colors.print(Colors.OKBLUE, "将对 %s 下的目录名进行替换操作，目录中源字符 %s 将替换为 %s，预计处理目录共 %s 条，目录信息如下，请确认"%(rootPath, sourceName, targetName, len(dirNames)))
        for dirPath in dirNames:
            Colors.print(Colors.OKBLUE, os.path.join(rootPath, dirPath))
        choise = input("是否继续执行操作[Y/N]：")
        if "Y" == choise.upper():
            logger = LoggerUtil().getLogger('目录操作-批量目录名替换字段')
            for dirPath in dirNames:
                oldName = os.path.join(rootPath, dirPath)
                newName = os.path.join(rootPath, dirPath.replace(sourceName, targetName))
                os.rename(oldName, newName)
                logger.info("成功将 %s 重命名为 %s"%(oldName, newName))
        elif "N" == choise.upper():
            return
        else:
            Colors.print(Colors.FAIL, "输入选项不合法！")
            return
