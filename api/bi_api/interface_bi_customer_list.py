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


class interfaceBiCustomerList(Resource):
    @api_version
    # @login_required
    def post(self, version):
        xml = request.args.get('format')
        try:
            body = modelEnum.user.value.get('body')
            request_data = req.request_process(request, xml, modelEnum.user.value)

            must = req.verify_one_param_must_empty(request_data, 'user_id')
            if must:
                return response_result_process(must, xml=xml)

            user_id = int(request_data.get('user_id'))
            g.user_id = user_id

            current_page = request_data.get('current_page')
            current_page_type = req.verify_one_param_type('current_page', current_page, int)
            if current_page_type:
                return response_result_process(current_page_type, xml=xml)
            if int(current_page) <= 0:
                current_page = 1

            page_size = request_data.get('page_size')
            page_size_type = req.verify_one_param_type('page_size', page_size, int)
            if page_size_type:
                return response_result_process(page_size_type, xml=xml)
            if int(page_size) <= 0:
                page_size = 200

            search = {'search_name': request_data.get('search_name'),
                      'search_mobile': request_data.get('search_mobile'),
                      'is_sfsc': request_data.get('is_sfsc')}

            data = bi_api_singleton.get_customer_list(int(current_page), int(page_size), search)

            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
