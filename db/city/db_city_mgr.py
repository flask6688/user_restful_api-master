#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：fdzaxd
@file_name: db_city_mgr.py
@create date: 2019-10-27 15:07
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from common.common_time import get_system_datetime
from db.base import DbBase
from db.connection_pool1 import MysqlConn
from utils.log_helper import lg
import copy

from utils.status_code import response_code
from config import configuration

from werkzeug.security import generate_password_hash, check_password_hash


class DbCityMgr(DbBase):

    def get_city_list(self, num):
        """
        获取城市列表
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name('DB1')
            table_name = 'boc_city'
            fields = 'id,title'
            sql = self.create_select_sql(db_name, table_name, fields)
            print(sql)
            result = self.execute_fetch_all(db_conn, sql)
            print(result)
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()




city_mgr = DbCityMgr()
