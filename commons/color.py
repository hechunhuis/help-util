#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.logger_util import LoggerUtil
class Colors:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    logger = LoggerUtil().getLogger("console-log")

    @classmethod
    def print(self, color, text):
        printInfo = f"{color}{text}{self.ENDC}"
        print(printInfo)
        self.logger.info(printInfo)
        return printInfo