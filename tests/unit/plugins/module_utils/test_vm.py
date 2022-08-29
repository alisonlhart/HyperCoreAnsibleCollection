from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.scale_computing.hypercore.plugins.module_utils.vm import VM
from ansible_collections.scale_computing.hypercore.plugins.module_utils import errors

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestVM:
    def test_vm_from_ansible(self):
        vm_dict = dict(
            uuid=None,  # No uuid when creating object from ansible
            vm_name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="running",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system=None,
        )

        vm = VM(
            uuid=None,
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="running",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system=None,
        )

        assert vm == VM.from_ansible(vm_dict)

    def test_vm_from_hypercore_dict_is_not_none(self, rest_client):
        vm = VM(
            uuid="",  # No uuid when creating object from ansible
            node_uuid="412a3e85-8c21-4138-a36e-789eae3548a3",
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system=None,
            node_affinity={
                "strict_affinity": False,
                "preferred_node": None,
                "backup_node": None,
            },
        )

        vm_dict = dict(
            uuid="",
            nodeUUID="412a3e85-8c21-4138-a36e-789eae3548a3",
            name="VM-name",
            tags="XLAB-test-tag1,XLAB-test-tag2",
            description="desc",
            mem=42,
            state="RUNNING",
            numVCPU=2,
            netDevs=[],
            blockDevs=[],
            bootDevices=None,
            attachGuestToolsISO=False,
            operatingSystem=None,
            affinityStrategy={
                "strictAffinity": False,
                "preferredNodeUUID": "",
                "backupNodeUUID": "",
            },
        )

        vm_from_hypercore = VM.from_hypercore(vm_dict, rest_client)
        assert vm == vm_from_hypercore

    def test_vm_from_hypercore_dict_is_none(self, rest_client):
        vm = None
        vm_dict = None
        vm_from_hypercore = VM.from_hypercore(vm_dict, rest_client)
        assert vm == vm_from_hypercore

    def test_vm_to_hypercore(self):
        vm = VM(
            uuid=None,  # No uuid when creating object from ansible
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
        )

        assert vm.to_hypercore() == dict(
            name="VM-name",
            description="desc",
            mem=42,
            numVCPU=2,
            blockDevs=[],
            netDevs=[],
            bootDevices=[],
            tags="XLAB-test-tag1,XLAB-test-tag2",
            uuid=None,
            attachGuestToolsISO=False,
            operatingSystem="os_windows_server_2012",
            state="RUNNING",
        )

    def test_vm_to_ansible(self):
        vm = VM(
            uuid=None,  # No uuid when creating object from ansible
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="running",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
            node_affinity={
                "strict_affinity": True,
                "preferred_node": {
                    "node_uuid": "412a3e85-8c21-4138-a36e-789eae3548a3",
                    "backplane_ip": "10.0.0.1",
                    "lan_ip": "10.0.0.2",
                    "peer_id": 1,
                },
                "backup_node": {
                    "node_uuid": "f6v3c6b3-99c6-475b-8e8e-9ae2587db5fc",
                    "backplane_ip": "10.0.0.3",
                    "lan_ip": "10.0.0.4",
                    "peer_id": 2,
                },
            },
        )

        assert vm.to_ansible() == dict(
            uuid=None,  # No uuid when creating object from ansible
            vm_name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="running",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=[],
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
            node_affinity={
                "strict_affinity": True,
                "preferred_node": {
                    "node_uuid": "412a3e85-8c21-4138-a36e-789eae3548a3",
                    "backplane_ip": "10.0.0.1",
                    "lan_ip": "10.0.0.2",
                    "peer_id": 1,
                },
                "backup_node": {
                    "node_uuid": "f6v3c6b3-99c6-475b-8e8e-9ae2587db5fc",
                    "backplane_ip": "10.0.0.3",
                    "lan_ip": "10.0.0.4",
                    "peer_id": 2,
                },
            },
        )

    def test_find_disk(self):
        # TODO (domen): Write tests for find_disk, if necessary
        pass

    def test_create_payload_to_hc3(self):

        vm = VM(
            uuid=None,  # No uuid when creating object from ansible
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
        )

        assert vm.create_payload_to_hc3() == dict(
            options=dict(attachGuestToolsISO=False),
            dom=dict(
                name="VM-name",
                description="desc",
                mem=42,
                numVCPU=2,
                blockDevs=[],
                netDevs=[],
                bootDevices=[],
                tags="XLAB-test-tag1,XLAB-test-tag2",
                operatingSystem="os_windows_server_2012",
                state="RUNNING",
            ),
        )

    def test_update_payload_to_hc3(self):

        vm = VM(
            uuid=None,  # No uuid when creating object from ansible
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
        )

        assert vm.update_payload_to_hc3() == dict(
            dict(
                name="VM-name",
                description="desc",
                mem=42,
                numVCPU=2,
                blockDevs=[],
                netDevs=[],
                bootDevices=[],
                tags="XLAB-test-tag1,XLAB-test-tag2",
                uuid=None,
                operatingSystem="os_windows_server_2012",
                state="RUNNING",
            )
        )

    def test_equal_true(self):
        assert VM(
            uuid=None,  # No uuid when creating object from ansible
            node_uuid="412a3e85-8c21-4138-a36e-789eae3548a3",
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
            node_affinity={
                "strict_affinity": True,
                "preferred_node": {
                    "node_uuid": "412a3e85-8c21-4138-a36e-789eae3548a3",
                    "backplane_ip": "10.0.0.1",
                    "lan_ip": "10.0.0.2",
                    "peer_id": 1,
                },
                "backup_node": {
                    "node_uuid": "f6v3c6b3-99c6-475b-8e8e-9ae2587db5fc",
                    "backplane_ip": "10.0.0.3",
                    "lan_ip": "10.0.0.4",
                    "peer_id": 2,
                },
            },
        ) == VM(
            uuid=None,  # No uuid when creating object from ansible
            node_uuid="412a3e85-8c21-4138-a36e-789eae3548a3",
            name="VM-name",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
            node_affinity={
                "strict_affinity": True,
                "preferred_node": {
                    "node_uuid": "412a3e85-8c21-4138-a36e-789eae3548a3",
                    "backplane_ip": "10.0.0.1",
                    "lan_ip": "10.0.0.2",
                    "peer_id": 1,
                },
                "backup_node": {
                    "node_uuid": "f6v3c6b3-99c6-475b-8e8e-9ae2587db5fc",
                    "backplane_ip": "10.0.0.3",
                    "lan_ip": "10.0.0.4",
                    "peer_id": 2,
                },
            },
        )

    def test_equal_false(self):
        assert VM(
            uuid=None,  # No uuid when creating object from ansible
            name="VM-name",
            node_uuid="412a3e85-8c21-4138-a36e-789eae3548a3",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
            node_affinity={},
        ) != VM(
            uuid=None,  # No uuid when creating object from ansible
            name="VM   NAME    CHANGED !!!!!!",
            node_uuid="412a3e85-8c21-4138-a36e-789eae3548a3",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            description="desc",
            memory=42,
            power_state="started",
            vcpu=2,
            nics=[],
            disks=[],
            boot_devices=None,
            attach_guest_tools_iso=False,
            operating_system="os_windows_server_2012",
            node_affinity={},
        )

    def test_get_by_name(self, rest_client):
        ansible_dict = dict(
            vm_name="vm-name",
        )
        rest_client.get_record.return_value = dict(
            uuid="id",
            nodeUUID="node_id",
            name="VM-name-unique",
            tags="XLAB-test-tag1,XLAB-test-tag2",
            description="desc",
            mem=42,
            state="RUNNING",
            numVCPU=2,
            netDevs=[],
            blockDevs=[],
            bootDevices=None,
            attachGuestToolsISO=False,
            operatingSystem=None,
            affinityStrategy={
                "strictAffinity": False,
                "preferredNodeUUID": "",
                "backupNodeUUID": "",
            },
        )

        vm = VM(
            attach_guest_tools_iso=False,
            boot_devices=[],
            description="desc",
            disks=[],
            memory=42,
            name="VM-name-unique",
            nics=[],
            vcpu=2,
            operating_system=None,
            power_state="started",
            tags=["XLAB-test-tag1", "XLAB-test-tag2"],
            uuid="id",
            node_uuid="node_id",
            node_affinity={
                "strict_affinity": False,
                "preferred_node": None,
                "backup_node": None,
            },
        )

        vm_by_name = VM.get_by_name(ansible_dict, rest_client)
        assert vm == vm_by_name

    def test_get_or_fail_when_get(self, rest_client):
        rest_client.list_records.return_value = [
            {
                "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
                "nodeUUID": "",
                "name": "XLAB_test_vm",
                "blockDevs": [],
                "netDevs": [],
                "stats": "bla",
                "tags": "XLAB,test",
                "description": "test vm",
                "mem": 23424234,
                "state": "RUNNING",
                "numVCPU": 2,
                "bootDevices": [],
                "operatingSystem": "windows",
                "affinityStrategy": {
                    "strictAffinity": False,
                    "preferredNodeUUID": "",
                    "backupNodeUUID": "",
                },
            }
        ]
        actual = VM.from_hypercore(
            vm_dict=rest_client.list_records.return_value[0], rest_client=rest_client
        ).to_hypercore()
        results = VM.get_or_fail(
            query={"name": "XLAB_test_vm"}, rest_client=rest_client
        )[0].to_hypercore()
        assert results == actual

    def test_get_or_fail_when_fail(self, rest_client):
        rest_client.list_records.return_value = []
        with pytest.raises(
            errors.VMNotFound,
            match="Virtual machine - {'name': 'XLAB-test-vm'} - not found",
        ):
            VM.get_or_fail(query={"name": "XLAB-test-vm"}, rest_client=rest_client)


class TestNic:
    @classmethod
    def _get_test_vm(cls, rest_client):
        nic_dict_1 = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "virDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "vlan": 1,
            "type": "virtio",
            "macAddress": "12-34-56-78-AB",
            "ipv4Addresses": ["10.0.0.1", "10.0.0.2"],
            "connected": True,
        }
        nic_dict_2 = {
            "uuid": "6456f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "virDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "vlan": 2,
            "type": "RTL8139",
            "vlan_new": 1,
            "macAddress": "12-34-56-78-CD",
            "ipv4Addresses": ["10.0.0.1", "10.0.0.2"],
            "connected": True,
        }
        return VM.from_hypercore(
            {
                "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
                "nodeUUID": "",
                "name": "XLAB_test_vm",
                "blockDevs": [],
                "netDevs": [nic_dict_1, nic_dict_2],
                "stats": "bla",
                "tags": "XLAB,test",
                "description": "test vm",
                "mem": 23424234,
                "state": "RUNNING",
                "numVCPU": 2,
                "bootDevices": [],
                "operatingSystem": "windows",
                "affinityStrategy": {
                    "strictAffinity": False,
                    "preferredNodeUUID": "",
                    "backupNodeUUID": "",
                },
            },
            rest_client,
        )

    def test_delete_unused_nics_to_hypercore_vm_when_no_delete(
        self, create_module, rest_client
    ):
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                items=[],
            )
        )
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "nodeUUID": "",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
            "affinityStrategy": {
                "strictAffinity": False,
                "preferredNodeUUID": "",
                "backupNodeUUID": "",
            },
        }
        rest_client.list_records.return_value = [vm_dict]
        virtual_machine = VM.get(
            query={"name": module.params["vm_name"]}, rest_client=rest_client
        )[0]
        results = virtual_machine.delete_unused_nics_to_hypercore_vm(
            module.params, rest_client
        )
        assert results is False

    def test_delete_unused_nics_to_hypercore_vm_when_one_nic_deleted(
        self, create_module, rest_client
    ):
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                items=[],
            )
        )
        nic_dict = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "virDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "vlan": 1,
            "type": "virtio",
            "macAddress": "12-34-56-78-CD",
            "ipv4Addresses": ["10.0.0.1", "10.0.0.2"],
            "connected": True,
        }
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "nodeUUID": "",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [nic_dict],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
            "affinityStrategy": {
                "strictAffinity": False,
                "preferredNodeUUID": "",
                "backupNodeUUID": "",
            },
        }
        rest_client.list_records.return_value = [vm_dict]
        rest_client.delete_record.return_value = {"taskTag": "1234"}
        virtual_machine = VM.get(
            query={"name": module.params["vm_name"]}, rest_client=rest_client
        )[0]
        results = virtual_machine.delete_unused_nics_to_hypercore_vm(
            module.params, rest_client
        )
        assert results is True

    def test_delete_unused_nics_to_hypercore_vm_when_multiple_nic_deleted(
        self, create_module, rest_client
    ):
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                items=[],
            )
        )
        nic_dict_1 = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "virDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "vlan": 1,
            "type": "virtio",
            "macAddress": "00-00-00-00-00",
            "connected": True,
            "ipv4Addresses": ["10.0.0.1", "10.0.0.2"],
        }
        nic_dict_2 = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "virDomainUUID": "8542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "vlan": 2,
            "type": "virtio",
            "macAddress": "00-00-00-00-00",
            "connected": True,
            "ipv4Addresses": ["10.0.0.1", "10.0.0.2"],
        }
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "nodeUUID": "",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [nic_dict_1, nic_dict_2],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
            "affinityStrategy": {
                "strictAffinity": False,
                "preferredNodeUUID": "",
                "backupNodeUUID": "",
            },
        }
        rest_client.list_records.return_value = [vm_dict]
        rest_client.delete_record.side_effect = [
            {"taskTag": "1234"},
            {"taskTag": "5678"},
        ]
        virtual_machine = VM.get(
            query={"name": module.params["vm_name"]}, rest_client=rest_client
        )[0]
        results = virtual_machine.delete_unused_nics_to_hypercore_vm(
            module.params, rest_client
        )
        assert results is True

    def test_find_nic_vlan(self, rest_client):
        virtual_machine = self._get_test_vm(rest_client)
        results = virtual_machine.find_nic(vlan=1)
        assert results[1] is (None)
        assert results[0].vlan == 1
        assert results[0].mac == "12-34-56-78-AB"
        assert results[0].uuid == "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab"
        assert results[0].vm_uuid == "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg"
        assert results[0].connected is True

    def test_find_nic_vlan_and_vlan_new(self, rest_client):
        virtual_machine = self._get_test_vm(rest_client)
        results = virtual_machine.find_nic(vlan=2, vlan_new=1)
        print(results)
        assert results[0].vlan == 2
        assert results[0].mac == "12-34-56-78-CD"
        assert results[0].uuid == "6456f2hj-6u9a-90ff-6g91-7jeahgf47aab"
        assert results[0].vm_uuid == "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg"
        assert results[0].connected is True
        assert results[1].vlan == 1
        assert results[1].mac == "12-34-56-78-AB"
        assert results[1].uuid == "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab"
        assert results[1].vm_uuid == "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg"
        assert results[1].connected is True

    def test_find_nic_mac(self, rest_client):
        virtual_machine = self._get_test_vm(rest_client)
        results = virtual_machine.find_nic(mac="12-34-56-78-CD")
        print(results)
        assert results[0].vlan == 2
        assert results[0].mac == "12-34-56-78-CD"
        assert results[0].uuid == "6456f2hj-6u9a-90ff-6g91-7jeahgf47aab"
        assert results[0].vm_uuid == "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg"
        assert results[0].connected is True

    def test_find_nic_mac_and_mac_new(self, rest_client):
        virtual_machine = self._get_test_vm(rest_client)
        results = virtual_machine.find_nic(
            mac="12-34-56-78-CD", mac_new="12-34-56-78-AB"
        )
        print(results)
        assert results[0].vlan == 2
        assert results[0].mac == "12-34-56-78-CD"
        assert results[0].uuid == "6456f2hj-6u9a-90ff-6g91-7jeahgf47aab"
        assert results[0].vm_uuid == "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg"
        assert results[0].connected is True
        assert results[1].vlan == 1
        assert results[1].mac == "12-34-56-78-AB"
        assert results[1].uuid == "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab"
        assert results[1].vm_uuid == "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg"
        assert results[1].connected is True
