#!/usr/bin/env python
#--*-- coding:utf-8 --*--

import ConfigParser
import MySQLdb
from DBUtils.PooledDB import PooledDB

class heimdalldb(object):

    def __init__(self):
        '''
        Read db config
        '''
        config = ConfigParser.ConfigParser()
        config.read('./utils/dbcfg.conf')
        self.host = config.get("MYSQLDB", "host")
        self.port = config.get("MYSQLDB", "port")
        self.username = config.get("MYSQLDB", "username")
        self.password = config.get("MYSQLDB", "password")
        self.dbname = config.get("MYSQLDB", "dbname")
        self.chrset = config.get("MYSQLDB", "chrset")
        self.conn = PooledDB(MySQLdb,host=self.host,user=self.username,passwd=self.password,db=self.dbname,port=int(self.port),charset=self.chrset).connection()

    def insertbysql(self, sql):
        '''
        insert by sql
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            return "None"
        finally:
            cursor.close()

    def getbysql(self, sql):
        '''
        Get by sql
        :param sql:
        :param param:
        :return:
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as e:
            return "None"
        finally:
            cursor.close()


    def __del__(self):
        self.conn.close()
