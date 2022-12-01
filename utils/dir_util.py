#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   created     ： 2022年11月24日 10:05
   filename    ： DirUtil.py
   author      :  hechunhui
   email       :  hechunhui_email@163.com
   Description :  目录操作工具类
"""
__author__ = 'hechunhui'

import os

class DirUtil:

    @classmethod
    def getSubName(self, parentPath:str):
        '''
        根据路径，获取子目录数组
        Args:
            parentPath:父路径
        Returns：
            subPath:直属子路径数组
        '''
        return os.listdir(parentPath)

    @classmethod
    def filteDirPath(self, prePath, sourceNames):
        '''
        过滤并返回prePath下的目录路径
        Args:
            prePath:前置路径
            sourceNames：目录名称集合
        Returns：
            dirPaths:目录路径集合
        '''
        if len(sourceNames) == 0:
            return sourceNames
        dirNames = []
        for sourceName in sourceNames:
            if os.path.isdir(os.path.join(prePath, sourceName)):
                dirNames.append(sourceName)
        return dirNames
    
    @classmethod
    def filterFilePath(self, prePath, suffixInfos):
        '''
        获取prePath下，后缀名为suffixInfo的路径集合
        Args：
            prePath:前置路径
            suffixInfo:文件后缀名,例如：['.xlsx','.xls']
        Returns：
            filePaths：符合条件的文件路径集合
        '''
        filePaths = []
        if prePath == None or suffixInfos == None or len(suffixInfos) == 0:
            return filePaths
        allPaths = self.getSubName(prePath)
        if allPaths == None or len(allPaths) == 0:
            return filePaths
        for path in allPaths:
            for suffixInfo in suffixInfos:
                if path.endswith(suffixInfo):
                    filePaths.append(os.path.join(prePath, path))
        return filePaths