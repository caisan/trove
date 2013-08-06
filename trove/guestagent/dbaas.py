# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2011 OpenStack, LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Handles all processes within the Guest VM, considering it as a Platform

The :py:class:`GuestManager` class is a :py:class:`nova.manager.Manager` that
handles RPC calls relating to Platform specific operations.

**Related Flags**

"""

import os

from trove.openstack.common import log


LOG = log.getLogger(__name__)
SERVICE_REGISTRY = {
    'mysql': 'trove.guestagent.manager.mysql.Manager',
    'percona': 'trove.guestagent.manager.mysql.Manager',
}


def to_gb(bytes):
    if bytes == 0:
        return 0.0
    size = bytes / 1024.0 ** 3
    return round(size, 2)


def get_filesystem_volume_stats(fs_path):
    try:
        stats = os.statvfs(fs_path)
    except OSError:
        LOG.exception("Error getting volume stats.")
        raise RuntimeError("Filesystem not found (%s)" % fs_path)

    total = stats.f_blocks * stats.f_bsize
    free = stats.f_bfree * stats.f_bsize
    # return the size in GB
    used = to_gb(total - free)

    output = {
        'block_size': stats.f_bsize,
        'total_blocks': stats.f_blocks,
        'free_blocks': stats.f_bfree,
        'total': total,
        'free': free,
        'used': used
    }
    return output