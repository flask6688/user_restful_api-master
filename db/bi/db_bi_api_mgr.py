#!/usr/bin/python
# -*- coding: UTF-8 -*
from itertools import groupby
from operator import itemgetter

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
        获取客户列表
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
            print(len(search['is_sfsc']))
            if len(search['is_sfsc']) > 0 and int(search['is_sfsc']) == 1:
                condition += ' and NOT ISNULL( tb_user_sfsc.is_del )'
            elif len(search['is_sfsc']) > 0 and int(search['is_sfsc']) == 0:
                condition += ' and ISNULL( tb_user_sfsc.is_del )'

            condition = condition.strip(' ').strip('and')

            if len(condition) == 0:
                condition = None

            relations = [{'table_name': 'tb_user_sfsc', 'join_condition': 'tb_customer.id = tb_user_sfsc.customer_id and tb_user_sfsc.user_id='+str(g.user_id)}]

            sql_count, sql = self.create_get_relation_page_sql_where(db_name, 'tb_customer',
                                                               'tb_customer.*,	tb_user_sfsc.is_del ', relations,
                                                               start_num, page_size,
                                                               condition)
            # print(sql, sql_count)
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
                data = self.del_favorites(user)
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

    def get_bc_details_by_id(self, type,id):
        """
        给前端使用的通过id获取行为细查详情
        :return:
        """
        conn = MysqlConn()
        try:

            db_name = configuration.get_database_name()

            if (type == 'gm'):

                salesOrg = '1002'
                condition = 'lsxhdddmx.id="%s" and a.ZXSZZBM = "%s"' % (id, salesOrg)
                gm_relations = [{"table_name": "ztsd_064 as a", "join_condition": "a.ZWLBM=lsxhdddmx.goods_sn"}]
                fields = 'lsxhdddmx.lylx_name,lsxhdddmx.shipping_time_ck,lsxhdddmx.receiver_name,lsxhdddmx.receiver_mobile,lsxhdddmx.receiver_address,a.ZYJPL,a.ZEJPL,a.ZXINH'
                gm_query_sql = self.create_get_relation_sql(db_name, "lsxhdddmx", fields, gm_relations,condition=condition)

                data = response_code.SUCCESS
                data['data'] = self.execute_fetch_all(conn, gm_query_sql)

            elif (type == 'sh'):

                sh_relations = [{"table_name": "tb_C4C_CLASS as a",
                                 "join_condition": "a.class_id=tb_c4c_order_xq.ServiceIssueCategoryID"},
                                {"table_name": "tb_C4C_CLASS as b",
                                 "join_condition": "b.class_id=tb_c4c_order_xq.IncidentServiceIssueCategoryID"},
                                {"table_name": "tb_C4C_CLASS as c",
                                 "join_condition": "c.class_id=tb_c4c_order_xq.ActivityServiceIssueCategoryID"}]

                condition = 'tb_c4c_order_xq.id=%s' % id
                fields = 'tb_c4c_order_xq.id,tb_c4c_order_xq.ZProCategory_KUTText,tb_c4c_order_xq.ZProductModel_KUTText,a.CLASS_NAME Servicecategory,b.CLASS_NAME Faultdescription,c.CLASS_NAME Maintenancemeasures'
                sh_query_sql = self.create_get_relation_sql(db_name, "tb_c4c_order_xq", fields, sh_relations,condition=condition)

                data = response_code.SUCCESS
                data['data'] = self.execute_fetch_all(conn, sh_query_sql)

            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
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

    def del_favorites(self, user_json):
        """
        删除收藏信息
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

            create_delete_sql = self.create_delete_sql(db_name, 'tb_user_sfsc', condition)
            self.delete_exec(conn, create_delete_sql)

            # 返回
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def get_customer_detail(self, customer_id):
        """
        获取客户详情
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name('DB')

            # 客户基础信息 tb_customer
            tb_customer_sql = self.create_select_sql(db_name, 'tb_customer', 'receiver_name,receiver_mobile,receiver_address,shipping_time_ck',
                                                     'id ='+str(customer_id))
            tb_customer_data = self.execute_fetch_one(conn, tb_customer_sql)
            # 客户最终表 tb_customer_zzb
            tb_customer_zzb_sql = self.create_select_sql(db_name, 'tb_customer_zzb', 'xfptph,spph,PJKDL,PJGMJS,XFJG,XFPC,xfrph,dchdph,RFM,XDCS',
                                                         'receiver_mobile = "'+str(tb_customer_data.get('receiver_mobile')) + '"')
            tb_customer_zzb_data = self.execute_fetch_one(conn, tb_customer_zzb_sql)
            # 售后最终表 tb_c4c_order_zzb
            tb_c4c_order_zzb_sql = self.create_select_sql(db_name, 'tb_c4c_order_zzb','WXCS,WXFSPH,WXCP',
                                                         'receiver_mobile = "' + str(tb_customer_data.get('receiver_mobile')) + '"')
            tb_c4c_order_zzb_data = self.execute_fetch_one(conn, tb_c4c_order_zzb_sql)
            # 统计客户购买产品及其次数
            tb_lsxhdddmx_sql = self.create_select_sql(db_name, 'lsxhdddmx','goods_name,COUNT(goods_id) num',
                                                     'receiver_mobile="'+str(tb_customer_data.get('receiver_mobile'))+ '" GROUP BY goods_id')
            tb_lsxhdddmx_data = self.execute_fetch_all(conn, tb_lsxhdddmx_sql)

            customer_info = {}
            # 用户概览
            customer_info['overview'] = {
                'shipping_time_ck': tb_customer_data.get('shipping_time_ck'),
                'RFM': tb_customer_zzb_data.get('RFM'),
                'XDCS': tb_customer_zzb_data.get('XDCS'),
                'repairs_num': 0,
                'already_purchase': tb_lsxhdddmx_data
            }
            # 用户基础
            customer_info['customer_info'] = {
                'name': tb_customer_data.get('receiver_name'),
                'address': tb_customer_data.get('receiver_address'),
                'email': None,
                'icon': None,
                'sex': None,
                'age': None
            }
            # 会员信息
            customer_info['member_info'] = {}
            # 消费信息
            customer_info['purchase_info'] = {
                'XDCS': tb_customer_zzb_data.get('XDCS'),
                'RFM': tb_customer_zzb_data.get('RFM'),
                'XFPC': tb_customer_zzb_data.get('XFPC')
            }
            # 售后信息
            numbers = {
                "121": "上门", "122": "送修", "123": "寄修", "163": "微信配件商城订单"
            }
            if tb_c4c_order_zzb_data:
                tb_c4c_order_zzb_data['WXFSPH'] = numbers.get(tb_c4c_order_zzb_data['WXFSPH'])

            customer_info['sh_info'] = {
                'WXCS': tb_c4c_order_zzb_data.get('WXCS'),
                'WXFSPH': tb_c4c_order_zzb_data.get('WXFSPH'),
                'WXCP': tb_c4c_order_zzb_data.get('WXCP'),
            }
            # 咨询
            customer_info['consult_info'] = {}

            data = response_code.SUCCESS
            data['data'] = customer_info
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_customer_action(self, customer_id, t):
        """
        获取客户行为 type 1购买 2售后
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name('DB')

            # 客户基础信息 tb_customer
            tb_customer_sql = self.create_select_sql(db_name, 'tb_customer', 'receiver_mobile',
                                                     'id ='+str(customer_id))
            tb_customer_data = self.execute_fetch_one(conn, tb_customer_sql)

            # 购买信息 lsxhdddmx
            lsxhdddmx_sql = self.create_select_sql(db_name, 'lsxhdddmx', 'id,shipping_time_ck as day,goods_name,lylx_name,1 as type',
                                                       'receiver_mobile = "'+ str(tb_customer_data.get('receiver_mobile')) + '"')
            lsxhdddmx_data = self.execute_fetch_all(conn, lsxhdddmx_sql)

            # 售后信息 tb_c4c_order_xq
            tb_c4c_order_xq_sql = self.create_select_sql(db_name, 'tb_c4c_order_xq', 'id,DATE_FORMAT(WXSJ,"%Y%m%d") as day,WXCP,WXFS,2 as type',
                                                         'receiver_mobile="'+ str(tb_customer_data.get('receiver_mobile')) + '"')
            tb_c4c_order_xq_data = self.execute_fetch_all(conn, tb_c4c_order_xq_sql)

            numbers = {
                "121": "上门", "122": "送修", "123": "寄修", "163": "微信配件商城订单"
            }
            for key in tb_c4c_order_xq_data:
                key['WXFS'] = numbers.get(key['WXFS'])

            res = []
            if int(t) == 1:
                res = lsxhdddmx_data
            elif int(t) == 2:
                res = tb_c4c_order_xq_data
            else:
                res = lsxhdddmx_data + tb_c4c_order_xq_data

            res.sort(key=itemgetter('day'))
            result = dict()
            for issue_id, items in groupby(res, key=itemgetter('day')):
                result[str(issue_id)] = list(items)

            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

db_bi_api_mgr = DbBiApiMgr()
