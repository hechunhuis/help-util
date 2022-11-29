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
        过滤目录文件
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