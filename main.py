#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from service.system_service import SystemService
from commons.color import Colors
import sys,os

systemService = SystemService()
while True:
    systemService.runMethod(systemService.menuController())
    Colors.print(Colors.OKGREEN, "\n程序执行完成")
    while True:
            choise = input("\n是否返回主菜单[Y/N]:")
            if "Y" == choise.upper():
                os.system('cls || clear')
                break
            elif "N" == choise.upper():
                sys.exit()
            else:
                Colors.print(Colors.FAIL, "输入选项不合法,请重新输入！")
