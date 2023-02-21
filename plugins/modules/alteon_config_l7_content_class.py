#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Radware LTD.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: alteon_config_l7_content_class
short_description: create and manage layer7 content class in Radware Alteon
description:
  - create and manage layer7 content class in Radware Alteon.
version_added: '2.9'
author:
  - Michal Greenberg (@michalg)
options:
  provider:
    description:
      - Radware Alteon connection details.
    required: true
    type: dict
    suboptions:
      server:
        description:
          - Radware Alteon IP address.
        required: true
        default: null
        type: str
      user:
        description:
          - Radware Alteon username.
        required: true
        default: null
        type: str
      password:
        description:
          - Radware Alteon password.
        required: true
        default: null
        type: str
        aliases:
        - pass
        - pwd
      validate_certs:
        description:
          - If C(no), SSL certificates will not be validated.
          - This should only set to C(no) used on personally controlled sites using self-signed certificates.
        required: true
        default: true
        type: bool
      https_port:
        description:
          - Radware Alteon https port.
        required: true
        default: 443
        type: int
      ssh_port:
        description:
          - Radware Alteon ssh port.
        required: true
        default: 22
        type: int
      timeout:
        description:
          - Timeout for connection.
        required: true
        default: 20
        type: int
  state:
    description:
      - When C(present), guarantees that the object exists with the provided attributes.
      - When C(absent), when applicable removes the object.
      - When C(read), when exists read object from configuration to parameter format.
      - When C(overwrite), removes the object if exists then recreate it. This state can be used only before applying the entry.
        If the entry was already applied you must delete, apply and recreate the entry.
      - When C(append), append object configuration with the provided parameters
    required: true
    default: null
    type: str
    choices:
    - present
    - absent
    - read
    - overwrite
    - append
  revert_on_error:
    description:
      - If an error occurs, perform revert on alteon.
    required: false
    default: false
    type: bool
  write_on_change:
    description:
      - Executes Alteon write calls only when an actual change has been evaluated.
    required: false
    default: false
    type: bool
  parameters:
    description:
      - Parameters for layer7 content class configuration.
    type: dict
    suboptions:
      content_class_id:
        description:
          - content class index.
        required: true
        default: null
        type: str
      name:
        description:
          - Set Descriptive name for the content class.
        required: false
        default: null
        type: str
      content_class_type:
        description:
          - The content class type. This field can be set only for new entry.
        required: false
        default: null
        type: str
        choices:
        - http
        - http2
        - ssl
      logical_expression:
        description:
          - Set logical expression between classes.
        required: false
        default: null
        type: str
      host_name:
        description:
          - Read only field to indicate if URL host name table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      path:
        description:
          - Read only field to indicate if URL path table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      file_name:
        description:
          - Read only field to indicate if URL file name table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      file_type:
        description:
          - Read only field to indicate if URL file_type table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      header:
        description:
          - Read only field to indicate if header table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      cookie:
        description:
          - Read only field to indicate if cookie table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      text:
        description:
          - Read only field to indicate if text table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
      xml_tag:
        description:
          - Read only field to indicate if xml_tag table is not empty for current content class.
        required: false
        default: null
        type: str
        choices:
        - "yes"
        - "no"
notes:
  - Requires the Radware alteon-sdk Python package on the host. This is as easy as
      C(pip3 install alteon-sdk)
requirements:
  - alteon-sdk
'''

EXAMPLES = r'''
- name: alteon configuration command
  radware.alteon.alteon_config_l7_content_class:
    provider:
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: no
      https_port: 443
      ssh_port: 22
      timeout: 5
    state: present
    parameters:
      content_class_id: 3
      name: content_class3
      content_class_type: http2
'''

RETURN = r'''
status:
  description: Message detailing run result
  returned: success
  type: str
  sample: object deployed successfully
obj:
  description: parameters object type
  returned: changed, read
  type: dict
'''

from ansible.module_utils.basic import AnsibleModule
import traceback
import logging

from ansible_collections.radware.alteon.plugins.module_utils.common import RadwareModuleError
from ansible_collections.radware.alteon.plugins.module_utils.alteon import AlteonConfigurationModule, \
    AlteonConfigurationArgumentSpec as ArgumentSpec
from radware.alteon.sdk.configurators.l7_content_class import L7ContentClassConfigurator


class ModuleManager(AlteonConfigurationModule):
    def __init__(self, **kwargs):
        super().__init__(L7ContentClassConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(L7ContentClassConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    # logging.basicConfig(filename="logL7cntclss7.txt", filemode='a',
    #      format='[%(levelname)s %(asctime)s %(filename)s:%(lineno)s %(funcName)s]\n%(message)s',
    #      level=logging.DEBUG, datefmt='%d-%b-%Y %H:%M:%S')
    # log = logging.getLogger()

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
