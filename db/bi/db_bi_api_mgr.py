#!/usr/bin/python
# -*- coding: UTF-8 -*
from flask import g

from common.common_time import get_system_datetime
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.log_helper import lg
import copy

from utils.status_code import response_code
from config import configuration

from werkzeug.security import generate_password_hash, check_password_hash


class DbBiApiMgr(DbBase):

    def get_customer_list(self, current_page, page_size, search):
        """
        获取用户
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name('DB')
            start_num = (current_page - 1) * page_size

            # 添加查询条件
            condition = ' '
            if search['search_name']:
                condition += ' tb_customer.receiver_name like "%' + search['search_name'] + '%"'
            if search['search_mobile']:
                condition += ' and tb_customer.receiver_mobile like "%' + search['search_mobile'] + '%"'
            if search['is_sfsc']:
                condition += ' and tb_user_sfsc.is_del ="' + search['is_sfsc'] + '"'

            condition = condition.strip(' ').strip('and')

            if len(condition) == 0:
                condition = None

            relations = [{'table_name': 'tb_user_sfsc', 'join_condition': 'tb_customer.id = tb_user_sfsc.customer_id and tb_user_sfsc.user_id='+str(g.user_id)}]

            sql_count, sql = self.create_get_relation_page_sql_where(db_name, 'tb_customer',
                                                               'tb_customer.*,	tb_user_sfsc.is_del ', relations,
                                                               start_num, page_size,
                                                               condition)
            result = self.execute_fetch_pages(conn, sql_count, sql, current_page, page_size)

            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


db_bi_api_mgr = DbBiApiMgr()
