#!/usr/bin/python
# -*- coding: UTF-8 -*

from flask import request, g
from flask_restful import Resource

from common.common_log import operation_log
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_process import response_result_process

from core.bi_api_singleton import bi_api_singleton

from utils.api_version_verify import api_version
from utils.auth_helper import Auth
from utils.log_helper import lg
from utils.status_code import response_code


class interfaceBiApi(Resource):
    @api_version
    # @login_required
    def get(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            body = modelEnum.user.value.get('body')

            request_data = req.request_process(request, xml, modelEnum.user.value)
            # print(request_data.get('user_id'))
            current_page = request_data.get('current_page')
            page_size = request_data.get('page_size')
            search = {'search_name': request_data.get('search_name'),
                      'search_mobile': request_data.get('search_mobile'),
                      'is_sfsc': request_data.get('sfsc')}

            data = bi_api_singleton.get_customer_list(current_page, page_size, search)

            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
