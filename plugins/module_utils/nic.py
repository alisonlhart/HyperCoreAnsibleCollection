# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..module_utils.type import NicType


class Nic:
    def __init__(self):
        self.uuid = None
        self.vm_uuid = None
        self.type = None
        self.mac = None
        self.mac_new = None
        self.vlan = None
        self.vlan_new = None
        self.connected = None
        self.ipv4Addresses = []

    def __eq__(self, other):
        if self.vlan_new and not self.mac_new:
            return (
            self.vlan_new == other.vlan
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac == other.mac
            )
        elif other.vlan_new and not other.mac_new:
            return (
            self.vlan == other.vlan_new
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac == other.mac
            )
        elif self.mac_new and not self.vlan_new:
            return (
            self.vlan == other.vlan
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac_new == other.mac
            )
        elif other.mac_new and not other.vlan_new:
            return (
            self.vlan == other.vlan
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac == other.mac_new
            )
        elif self.vlan_new and self.mac_new:
            return (
            self.vlan_new == other.vlan
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac_new == other.mac
            )
        elif other.vlan_new and other.mac_new:
            return (
            self.vlan == other.vlan_new
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac == other.mac_new
            )
        return (
            self.vlan == other.vlan
            and self.type == other.type
            and self.vm_uuid == other.vm_uuid
            and self.mac == other.mac
        )

    @classmethod
    def handle_nic_type(cls, nic_type):
        if nic_type:
            if nic_type.upper() == NicType.INTEL_E1000:
                actual_nic_type = nic_type.upper()  # INTEL_E1000
            elif nic_type.upper() == NicType.VIRTIO:
                actual_nic_type = nic_type.lower()  # virtio
            else:
                actual_nic_type = nic_type.upper()  # RTL8139
            return actual_nic_type
        return nic_type

    # Compare two Network interfaces
    @classmethod
    def compare(cls, old_nic, new_nic):
        return new_nic == old_nic

    def data_to_hc3(self):
        nic_dict = {
            "vlan": self.vlan,
            "virDomainUUID": self.vm_uuid,
        }
        # TODO corner case: change vlan 0 -> 10, 10 -> 0. integration test
        if self.vlan_new is not None:
            nic_dict["vlan"] = self.vlan_new
        if self.type:
            nic_dict["type"] = self.type.upper()  # TODO enum
        if self.connected is not None:
            nic_dict["connected"] = self.connected
        if self.mac:  # if it's empty we don't send, it auto-generates
            nic_dict["macAddress"] = self.mac
        if self.mac_new:  # user wants to change mac address
            nic_dict["macAddress"] = self.mac_new
        return nic_dict

    def data_to_ansible(self):
        nic_info_dict = {
            "uuid": self.uuid,
            "vlan": self.vlan,
            "type": self.type,
            "mac": self.mac,
            "connected": self.connected,
            "ipv4_addresses": self.ipv4Addresses,
        }
        return nic_info_dict

    @classmethod
    def create_from_hc3(cls, nic_dict):
        obj = Nic()
        obj.uuid = nic_dict["uuid"]
        # HC3 API GET /VirDomain - we get virDomainUUID for each Nic
        # HC3 API GET /VirDomainNetDevice - virDomainUUID might be empty string
        obj.vm_uuid = nic_dict["virDomainUUID"]
        obj.type = Nic.handle_nic_type(nic_dict.get("type", None))
        obj.mac = nic_dict.get("macAddress", None)
        obj.vlan = nic_dict.get("vlan", 0)
        obj.connected = nic_dict.get("connected", True)
        obj.ipv4Addresses = nic_dict.get("ipv4Addresses", [])
        return obj

    @classmethod
    def create_from_ansible(cls, nic_dict):
        obj = Nic()
        obj.vm_uuid = nic_dict.get("vm_uuid", None)
        obj.type = Nic.handle_nic_type(nic_dict.get("type", None))
        obj.mac = nic_dict.get("mac", None)
        obj.mac_new = nic_dict.get("mac_new", None)
        obj.vlan = nic_dict["vlan"]
        obj.vlan_new = nic_dict.get("vlan_new", None)
        return obj
