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


class interfaceBiFavorites(Resource):

    @api_version
    #@login_required
    def post(self, version, user_id=None):
        xml = request.args.get('format')
        try:
            if user_id is not None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.user.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['user_id', 'customer_id']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            data = bi_api_singleton.add_favorites(request_data)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

