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


class interfaceBiCustomerAction(Resource):
    @api_version
    # @login_required
    def get(self, version):
        xml = request.args.get('format')
        try:
            body = modelEnum.user.value.get('body')

            if request.args.get('customer_id') is None:
                return {'code': 400, 'msg': 'customer_id is required'}
            customer_id = request.args.get('customer_id')
            if len(customer_id) <= 0:
                return {'code': 400, 'msg': 'customer_id is required'}

            data = bi_api_singleton.get_customer_action(customer_id)

            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)
