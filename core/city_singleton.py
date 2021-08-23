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

from db.city.db_city_mgr import city_mgr

__all__ = {"CitySingleton"}


class CitySingleton:
    """"
    """

    def get_city_list(self, num=10):
        """
        获取所有用户信息
        :return:返回用户信息json
        """

        return city_mgr.get_city_list(num)


city_singleton = CitySingleton()
