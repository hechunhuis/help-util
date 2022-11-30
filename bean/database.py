#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser

class Database:
    config = None
    configPath = None
    host = None
    port = None
    dbName = None
    tableName = None
    username = None
    password = None

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.configPath = './configs/update_by_excel.ini'
        self.config.read(self.configPath, encoding='utf-8')
        self.host = self.config['database']['host']
        self.port = int(self.config['database']['port'])
        self.dbName = self.config['database']['dbName']
        self.username = self.config['database']['username']
        self.password = self.config['database']['password']
        self.tableName = self.config['database']['tableName']

    def toString(self):
        return 'host:%s prot:%s dbName:%s username:%s password:%s'%(self.host, self.port, self.dbName, self.username, self.password)