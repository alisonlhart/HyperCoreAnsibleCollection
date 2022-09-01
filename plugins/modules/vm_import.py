#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: vm_import

author:
  - Domen Dobnikar (@domen_dobnikar)
short_description: Plugin handles import of the virtual machine.
description:
  - Plugin enables import of the virtual machine, from a specified location.
version_added: 0.0.1
extends_documentation_fragment:
  - scale_computing.hypercore.cluster_instance
seealso: []
options:
  vm_name:
    description:
      - Virtual machine name.
      - Used to identify selected virtual machine by name.
    type: str
    required: true
  smb:
    description:
      - SMB server, access and location data.
      - Source, username, password
    type: dict
    required: true
    suboptions:
      server:
        type: str
        description:
          - Specified SMB server, where the selected virtual machine is to be imported from.
        required: true
      path:
        type: str
        description:
          - Specified location on the SMB server, where the exported virtual machine is to be imported from.
        required: true
      username:
        type: str
        description:
          - Username.
        required: true
      password:
        type: str
        description:
          - Password.
        required: true
  cloud_init:
    description:
      - Configuration to be used by cloud-init (Linux) or cloudbase-init (Windows).
      - When non-empty will create an extra ISO device attached to VirDomain as a NoCloud datasource.
    required: false
    type: dict
    suboptions:
      user_data:
        description:
          - Configuration user-data to be used by cloud-init (Linux) or cloudbase-init (Windows).
          - Valid YAML syntax.
        type: str
      meta_data:
        type: str
        description:
          - Configuration meta-data to be used by cloud-init (Linux) or cloudbase-init (Windows).
          - Valid YAML syntax.
"""

EXAMPLES = r"""
- name: import VM from SMB
  scale_computing.hypercore.vm_import:
    vm_name: demo-vm
    smb:
      server: demo-smb-server
      path: /share/path/to/vms/demo-vm-exported-v0
      username: user
      password: pass
  register: output

- name: import VM from SMB with cloud init data added
  scale_computing.hypercore.vm_import:
    vm_name: demo-vm
    smb:
      server: demo-smb-server
      path: /share/path/to/vms/demo-vm-exported-v0
      username: user
      password: pass
    cloud_init:
      user_data: |
        valid:
        - yaml: 1
        - expression: 2
      meta_data: "{{ lookup('file', 'cloud-init-user-data-example.yml') }}"
  register: output
"""

RETURN = r"""
msg:
  description:
    - Return message.
  returned: success
  type: str
  sample: Virtual machine - VM-TEST - import complete from - SMB-TEST
"""

from ansible.module_utils.basic import AnsibleModule
from ..module_utils import arguments, errors
from ..module_utils.client import Client
from ..module_utils.rest_client import RestClient
from ..module_utils.vm import VM
from ..module_utils.task_tag import TaskTag


def run(module, rest_client):
    virtual_machine_obj_list = VM.get(
        query={"name": module.params["vm_name"]}, rest_client=rest_client
    )
    if len(virtual_machine_obj_list) > 0:
        raise errors.DeviceNotUnique(module.params["vm_name"])
    task = VM.import_vm(rest_client, module.params)
    TaskTag.wait_task(rest_client, task)
    # Check if VM was imported and now exists
    VM.get_or_fail(query={"name": module.params["vm_name"]}, rest_client=rest_client)
    return True, "Virtual machine - {0} - import complete from - {1}".format(
        module.params["vm_name"], module.params["smb"]["server"]
    )


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("cluster_instance"),
            vm_name=dict(
                type="str",
                required=True,
            ),
            smb=dict(
                type="dict",
                required=True,
                options=dict(
                    server=dict(
                        type="str",
                        required=True,
                    ),
                    path=dict(
                        type="str",
                        required=True,
                    ),
                    username=dict(
                        type="str",
                        required=True,
                    ),
                    password=dict(
                        type="str",
                        no_log=True,
                        required=True,
                    ),
                ),
            ),
            cloud_init=dict(
                type="dict",
                default={},
                options=dict(
                    user_data=dict(type="str"),
                    meta_data=dict(type="str"),
                ),
            ),
        ),
    )

    try:
        host = module.params["cluster_instance"]["host"]
        username = module.params["cluster_instance"]["username"]
        password = module.params["cluster_instance"]["password"]

        client = Client(host, username, password)
        rest_client = RestClient(client=client)
        changed, msg = run(module, rest_client)
        module.exit_json(changed=changed, msg=msg)
    except errors.ScaleComputingError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
