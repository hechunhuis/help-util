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
    def getSubDirectory(parentPath:str):
        '''
        根据路径，获取子目录数组
        Args:
            parentPath:父路径
        Returns：
            subDirs:直属子目录数组
        '''
        dirs = os.listdir(parentPath)
        subDirs = []
        for dir in dirs:
            subDirs.append(parentPath + "\\" + dir)
        return subDirs