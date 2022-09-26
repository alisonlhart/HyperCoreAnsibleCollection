# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ..module_utils.utils import PayloadMapper
from ..module_utils import errors


class Disk(PayloadMapper):
    def __init__(
        self,
        type,
        slot,
        uuid=None,
        vm_uuid=None,
        cache_mode=None,
        size=None,
        name=None,
        disable_snapshotting=None,
        tiering_priority_factor=None,
        mount_points=None,
        read_only=None,
    ):
        self.uuid = uuid
        self.vm_uuid = vm_uuid
        self.type = type
        self.cache_mode = cache_mode
        self.size = size
        self.slot = slot
        self.name = name
        self.disable_snapshotting = disable_snapshotting
        self.tiering_priority_factor = tiering_priority_factor
        self.mount_points = mount_points
        self.read_only = read_only

    def to_hypercore(self):
        return dict(
            uuid=self.uuid,
            virDomainUUID=self.vm_uuid,
            type=self.type.upper(),
            cacheMode=self.cache_mode.upper() if self.cache_mode else None,
            capacity=self.size,
            slot=self.slot,
            name=self.name,
            disableSnapshotting=self.disable_snapshotting,
            tieringPriorityFactor=self.tiering_priority_factor,
            mountPoints=self.mount_points,
            readOnly=self.read_only,
        )

    def to_ansible(self):
        return dict(
            uuid=self.uuid,
            vm_uuid=self.vm_uuid,
            type=self.type,
            cache_mode=self.cache_mode,
            size=self.size,
            disk_slot=self.slot,
            iso_name=self.name,
            disable_snapshotting=self.disable_snapshotting,
            tiering_priority_factor=self.tiering_priority_factor,
            mount_points=self.mount_points,
            read_only=self.read_only,
        )

    @classmethod
    def from_hypercore(cls, hypercore_dict):
        if not hypercore_dict:
            return None
        try:
            return cls(
                uuid=hypercore_dict["uuid"],
                vm_uuid=hypercore_dict["virDomainUUID"],
                type=hypercore_dict["type"].lower(),
                cache_mode=hypercore_dict["cacheMode"].lower(),
                size=hypercore_dict["capacity"],
                slot=hypercore_dict["slot"],
                name=hypercore_dict["name"],
                disable_snapshotting=hypercore_dict["disableSnapshotting"],
                tiering_priority_factor=hypercore_dict["tieringPriorityFactor"],
                mount_points=hypercore_dict["mountPoints"],
                read_only=hypercore_dict["readOnly"],
            )
        except KeyError as e:
            raise errors.MissingValueHypercore(e)

    @classmethod
    def from_ansible(cls, ansible_dict):
        # Specific for this module - in case of performing PATCH method on the /VirDomainBlockDevice endpoint,
        # type_new is possible field if you want to update disk type. In that case, type_new is desired type
        # of the disk
        if ansible_dict.get("type_new", ""):
            disk_type = ansible_dict["type_new"]
        else:
            disk_type = ansible_dict["type"]
        # Only disk_type and slot are certainly going to be present in ansible_dict.
        # The rest of the fields may be specified if update action is performed
        # Ensure that size is integer
        if ansible_dict.get("size", None):
            size = int(ansible_dict["size"])
        else:
            size = None
        return cls(
            type=disk_type,
            slot=ansible_dict["disk_slot"],
            size=size,
            cache_mode=ansible_dict.get("cache_mode", None),
            name=ansible_dict.get("iso_name", None),
            disable_snapshotting=ansible_dict.get("disable_snapshotting", None),
            tiering_priority_factor=ansible_dict.get("tiering_priority_factor", None),
            mount_points=ansible_dict.get("mount_points", None),
            read_only=ansible_dict.get("read_only", None),
            uuid=ansible_dict.get("uuid", None),
        )

    def __eq__(self, other):
        """One Disk is equal to another if it has ALL attributes exactly the same. Used in tests only."""
        return all(
            (
                self.uuid == other.uuid,
                self.vm_uuid == other.vm_uuid,
                self.type == other.type,
                self.cache_mode == other.cache_mode,
                self.size == other.size,
                self.slot == other.slot,
                self.name == other.name,
                self.disable_snapshotting == other.disable_snapshotting,
                self.tiering_priority_factor == other.tiering_priority_factor,
                self.mount_points == other.mount_points,
                self.read_only == other.read_only,
            )
        )

    def __str__(self):
        return super().__str__()

    def post_payload(self, vm):
        # vm is object of class VM
        # vm will always have uuid property in the playbook
        return dict(
            {key: val for key, val in self.to_hypercore().items() if val},
            virDomainUUID=vm.uuid,
        )

    def patch_payload(self, vm, previous_disk):
        if self.tiering_priority_factor:
            tiering_priority_factor = self.tiering_priority_factor
        else:
            tiering_priority_factor = previous_disk.tiering_priority_factor
        return dict(
            {key: val for key, val in self.to_hypercore().items() if val},
            tieringPriorityFactor=tiering_priority_factor,
            virDomainUUID=vm.uuid,
        )