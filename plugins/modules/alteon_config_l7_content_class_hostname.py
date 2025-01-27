#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Radware LTD.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: alteon_config_l7_content_class_hostname
author:
  - Michal Greenberg (@michalg)
short_description: create and manage layer7 content class host name in Radware Alteon
description:
  - create and manage layer7 content class host name in Radware Alteon.
version_added: '1.0.0'
options:
  parameters:
    description:
      - Parameters for layer7 content class host name configuration.
    type: dict
    suboptions:
      content_class_id:
        description:
          - content class index.
        required: true
        default: null
        type: str
      host_name_id:
        description:
          - host name index.
        required: true
        default: null
        type: str
      host_name:
        description:
          - Set hostname to match.
        required: false
        default: null
        type: str
      match_type:
        description:
          - Set match type for content class host name.
        required: false
        default: null
        type: str
        choices:
        - sufx
        - prefx
        - equal
        - include
        - regex
        - unsupported
      data_class_id:
        description:
          - Set data class for hostname matching.
        required: false
        default: null
        type: str
extends_documentation_fragment:
  - radware.alteon.alteon_options_doc_fragment
  - radware.alteon.alteon_options_doc_fragment.other
  - radware.alteon.alteon_options_doc_fragment.state_type1
notes:
  - unsupported choice is read only
'''

EXAMPLES = r'''
- name: alteon configuration command
  radware.alteon.alteon_config_l7_content_class_hostname:
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
      host_name_id: host1
      host_name: test
      match_type: equal
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

from ansible_collections.radware.alteon.plugins.module_utils.common import RadwareModuleError
from ansible_collections.radware.alteon.plugins.module_utils.alteon import AlteonConfigurationModule, \
    AlteonConfigurationArgumentSpec as ArgumentSpec
try:
    from radware.alteon.sdk.configurators.l7_content_class_hostname import L7ContentClassHostNameConfigurator
except ModuleNotFoundError:
    if __name__ == '__main__':
        module_args = {'parameters': {'type': 'dict', 'required': False},
                       'provider': {'type': 'dict', 'required': True},
                       'revert_on_error': {'required': False, 'type': 'bool', 'default': False},
                       'write_on_change': {'required': False, 'type': 'bool', 'default': False},
                       'state': {'required': True, 'choices': ['present', 'absent', 'read', 'overwrite', 'append']}
                       }
        module = AnsibleModule(argument_spec=module_args, check_invalid_arguments=False)
        module.fail_json(msg="The alteon-sdk package is required")


class ModuleManager(AlteonConfigurationModule):
    def __init__(self, **kwargs):
        super().__init__(L7ContentClassHostNameConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(L7ContentClassHostNameConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    # logging.basicConfig(filename="logL7hostname.txt", filemode='a',
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
