#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
@author：li-boss
@file_name: resource.py
@create date: 2019-10-27 13:28 
@blog https://leezhonglin.github.io
@csdn https://blog.csdn.net/qq_33196814
@file_description：
"""
from flask_restful import Api

from api.department.interface_department import interfaceDepartment
from api.department.interface_department_staff import interfaceDepartmentStaff
from api.login.interface_login import interfaceLogin
from api.role.interface_permission import interfacePermission
from api.role.interface_role import interfaceRole
from api.role.interface_role_permission import interfaceRolePermission
from api.user.interface_basic import interfaceUserBasic
from api.user.interface_password import interfacePassword
from api.user.interface_user import interfaceUser
from api.user_group.interface_user_group import interfaceUserGroup
from api.user_group.interface_user_group_role import interfaceUserGroupRole
from api.user_group.interface_user_group_staff import interfaceUserGroupStaff
from api.bi_api.interface_bi_api import interfaceBiApi

api = Api()

# 部门管理
api.add_resource(
    interfaceDepartment,
    '/<version>/department',
    '/<version>/department/<int:dpt_id>'
)


api.add_resource(
    interfaceDepartmentStaff,
    '/<version>/department/staff/<int:dpt_id>'
)

# 用户
api.add_resource(
    interfaceUser,
    '/<version>/user',
    '/<version>/user/<int:user_id>',

)

# 密码
api.add_resource(
    interfacePassword,
    '/<version>/user/<int:user_id>/password'
)

# 基本信息修改
api.add_resource(
    interfaceUserBasic,
    '/<version>/user/<int:user_id>/base/info'
)

# 角色
api.add_resource(
    interfaceRole,
    '/<version>/role',
    '/<version>/role/<int:role_id>'
)
#  角色权限
api.add_resource(
    interfaceRolePermission,
    '/<version>/role/<role_id>/permission'
)
# 权限
api.add_resource(
    interfacePermission,
     '/<version>/permission'
)

# 用户组
api.add_resource(
    interfaceUserGroup,
    '/<version>/user/group',
    '/<version>/user/group/<int:group_id>'
)


api.add_resource(
    interfaceUserGroupStaff,
    '/<version>/user/group/<int:group_id>/staff'
)

# 获取用户组的角色信息
api.add_resource(
    interfaceUserGroupRole,
    '/<version>/user/group/<int:group_id>/role'
)

api.add_resource(
    interfaceLogin,
    '/<version>/login'
)

# text db1 获取boc_city
api.add_resource(
    interfaceBiApi,
    '/<version>/bi_api'
)