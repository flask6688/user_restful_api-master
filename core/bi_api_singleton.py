#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：fdzaxd
@file_name: user_singleton.py
@create date: 2019-10-27 15:03 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from db.bi.db_bi_api_mgr import db_bi_api_mgr

__all__ = {"BiApiSingleton"}


class BiApiSingleton:
    """"
    """

    def get_customer_list(self, current_page=1, page_size=100, search={}):
        """
        获取所有用户信息
        :return:返回用户信息json
        """

        return db_bi_api_mgr.get_customer_list(current_page, page_size, search)

    def add_favorites(self, user_info):
        """
        增加收藏
        :return:
        """
        return db_bi_api_mgr.add_favorites(user_info)

    def del_favorites(self, user_info):
        """
        取消收藏
        :return:
        """
        return db_bi_api_mgr.del_favorites(user_info)

    def get_customer_detail(self, customer_id):
        """
        获取用户详情信息
        :return:返回用户信息json
        """

        return db_bi_api_mgr.get_customer_detail(customer_id)

    def get_customer_action(self, customer_id, t):
        """
        获取用户行为细查
        :return:返回用户信息json
        """

        return db_bi_api_mgr.get_customer_action(customer_id, t)

    def get_bc_details_by_id(self, type, id):
        """
        通过ID获取行为细查各个数据
        :return: 返回当前JSON
        """
        return db_bi_api_mgr.get_bc_details_by_id(type, id)

bi_api_singleton = BiApiSingleton()
