#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: smtp_info

author:
  - Ana Zobec (@anazobec)
short_description: List SMTP configuration on HyperCore API.
description:
  - Use this module to list information about the SMTP configuration on HyperCore API.
version_added: 1.2.0
extends_documentation_fragment:
  - scale_computing.hypercore.cluster_instance
seealso:
  - module: scale_computing.hypercore.smtp
notes:
  - SMTP authentication can be configured using username and password.
    In this case the configured username is returned, but password is not.
    Returned password is always empty string ("").
"""


EXAMPLES = r"""
- name: List all configurations on DNS configuration on HyperCore API
  scale_computing.hypercore.smtp_info:
  register: smtp_info
"""

RETURN = r"""
record:
  description:
    - SMTP configuration record.
  returned: success
  type: dict
  contains:
    auth_user:
      description: Username for authentication if use_auth is true
      type: str
      sample: ""
    auth_password:
      description:
        - Password for authentication if use_auth is true.
        - HyperCore API currently does not allow retrieving configured SMPT password - returned password field contains emtpy string "".
          To be consistent module returned value is also empty string.
      type: str
      sample: ""
    from_address:
      description: Email address the system alerts will be sent from
      type: str
      sample: PUB6@scalecomputing.com
    latest_task_tag:
      description: Latest Task Tag
      type: dict
      sample:
        completed: 1675435601
        created: 1675435601
        descriptionParameters: []
        formattedDescription: Update Alert SMTP Config
        formattedMessage: ""
        messageParameters: []
        modified: 1675435601
        nodeUUIDs: []
        objectUUID: smtpconfig_guid
        progressPercent: 100
        sessionID: 92b4a736-259c-4f3c-9492-ce0c36691372
        state: COMPLETE
        taskTag: 761
    port:
      description: TCP port of the SMTP server
      type: int
      sample: 25
    server:
      description: IP address or hostname of the SMTP server
      type: str
      sample: smtp-relay.gmail.com
    use_auth:
      description: Is authentication enabled or not
      type: bool
      sample: false
    use_ssl:
      description: Enable SSL encryption
      type: bool
      sample: false
    uuid:
      description: Unique identifier
      type: str
      sample: smtpconfig_guid
"""


from ansible.module_utils.basic import AnsibleModule

from typing import Union, Dict, Any
from ..module_utils.typed_classes import TypedSmtpToAnsible
from ..module_utils import errors, arguments
from ..module_utils.client import Client
from ..module_utils.rest_client import RestClient
from ..module_utils.smtp import SMTP


def run(rest_client: RestClient) -> Union[TypedSmtpToAnsible, Dict[Any, Any]]:
    return SMTP.get_state(rest_client)


def main() -> None:
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
        ),
    )

    try:
        client = Client.get_client(module.params["cluster_instance"])
        rest_client = RestClient(client)
        record = run(rest_client)
        module.exit_json(changed=False, record=record)
    except errors.ScaleComputingError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
