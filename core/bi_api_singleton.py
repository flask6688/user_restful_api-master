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

        return db_bi_api_mgr.get_customer_list(int(current_page), int(page_size), search)


bi_api_singleton = BiApiSingleton()
