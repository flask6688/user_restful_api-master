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

    def get_favorites(self, user_id,customer_id):
        """
        条件查询收藏
        :param kwargs:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = 'user_id="%s" and customer_id="%s"' % (user_id, customer_id)

            sql = self.create_select_sql(db_name, 'tb_user_sfsc', '*', condition=condition)
            return self.execute_fetch_one(conn, sql)
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def add_favorites(self, user):
        """
        添加收藏
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # 解析参数成dict

            # 判断用户是否已经存在
            if_user = self.get_favorites(user_id=user['user_id'], customer_id=user['customer_id'])
            if if_user:
                data = self.upd_favorites(user)
                #data = response_code.RECORD_EXIST
                return data
            # 需要插入的字段
            fields = '(user_id,customer_id,is_del)'
            # 获取当前创建时间
            create_time = get_system_datetime()
            pass_word = generate_password_hash('123456')
            # 插入值
            value_tuple = (user['user_id'], user['customer_id'], user['is_del'])
            # 构造插入用户的sql语句
            insert_user_sql = self.create_insert_sql(db_name, 'tb_user_sfsc', fields, value_tuple)
            self.insert_exec(conn, insert_user_sql)

            data = response_code.SUCCESS

            return data

        except Exception as e:
            lg.error(e)
            conn.conn.rollback()
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()


    def upd_favorites(self,user_json):
        """
        更新收藏信息
        :param user:user json
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # 解析参数成dict
            user = user_json
            user_id = user.get('user_id')
            customer_id = user.get('customer_id')

            condition = 'user_id="%s" and customer_id="%s"' % (user_id, customer_id)

            # 更新用户基本信息
            update_user_fields = ['is_del']
            update_user_fields_value = [user.get('is_del')]
            update_user_sql = self.create_update_sql(db_name, 'tb_user_sfsc', update_user_fields, update_user_fields_value,
                                                     condition)
            self.updete_exec(conn, update_user_sql)

            # 返回
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            conn.close()



db_bi_api_mgr = DbBiApiMgr()
