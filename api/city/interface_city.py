#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: interface_login.py
@create date: 2019-10-27 14:36
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""

from flask import request, g
from flask_restful import Resource

from common.common_log import operation_log
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process

from core.city_singleton import city_singleton

from utils.api_version_verify import api_version
from utils.auth_helper import Auth
from utils.log_helper import lg
from utils.status_code import response_code


class interfaceCity(Resource):

    @api_version
    def get(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            body = modelEnum.user.value.get('body')

            request_data = req.request_process(request, xml, modelEnum.user.value)
                # print(request_data.get('user_id'))

            data = city_singleton.get_city_list()

            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
