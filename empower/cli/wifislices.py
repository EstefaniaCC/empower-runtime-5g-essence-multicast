#!/usr/bin/env python3
#
# Copyright (c) 2019 Roberto Riggio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""WiFi SLices CLI tools."""

import sys
import uuid
import argparse

import empower.cli.command as command


def pa_list_wifi_slices(args, cmd):
    """List wifi slices parser method."""

    usage = "%s <project_id>" % command.USAGE.format(cmd)
    desc = command.DESCS[cmd]
    (args, leftovers) = \
        argparse.ArgumentParser(usage=usage,
                                description=desc).parse_known_args(args)
    return args, leftovers


def do_list_wifi_slices(gargs, args, leftovers):
    """List wifi slices."""

    if len(leftovers) != 1:
        print("Invalid parameter, run help list-wifi-slices")
        command.print_available_cmds()
        sys.exit()

    project_id = uuid.UUID(leftovers[0])

    headers = command.get_headers(gargs)

    url = '/api/v1/projects/%s' % project_id
    _, prj = command.connect(gargs, ('GET', url), 200, headers=headers)

    url = '/api/v1/projects/%s/wifi_slices' % project_id
    _, slcs = command.connect(gargs, ('GET', url), 200, headers=headers)

    accum = []

    accum.append("project id ")
    accum.append(prj['project_id'])
    accum.append(" SSID ")

    if 'wifi_props' not in prj or not prj['wifi_props']:
        accum.append("UNDEFINED")
    else:
        accum.append(prj['wifi_props']['ssid'])

    for slc in slcs.values():

        accum.append("\nSlice ID: ")
        accum.append(str(slc['slice_id']))

        for k, val in slc['properties'].items():
            accum.append("\n    %s: %s" % (k, val))

    print(''.join(accum))


def pa_upsert_wifi_slice(args, cmd):
    """Create/update wifi slice parser method. """

    usage = "%s <project_id> <slice_id> <params>" % command.USAGE.format(cmd)
    desc = command.DESCS[cmd]
    (args, leftovers) = \
        argparse.ArgumentParser(usage=usage,
                                description=desc).parse_known_args(args)
    return args, leftovers


def do_upsert_wifi_slice(gargs, args, leftovers):
    """Create/update wifi slice. """

    params = command.get_params(leftovers)

    if len(leftovers) < 2:
        print("Invalid parameter, run help load-create-wifi-slice")
        command.print_available_cmds()
        sys.exit()

    project_id = uuid.UUID(leftovers[0])
    slice_id = int(leftovers[1])

    request = {
        "version": "1.0",
        "slice_id": slice_id
    }

    if params:
        request['properties'] = params

    headers = command.get_headers(gargs)

    url = '/api/v1/projects/%s/wifi_slices' % project_id
    command.connect(gargs, ('POST', url), 201, request, headers=headers)

    url = '/api/v1/projects/%s' % project_id
    _, prj = command.connect(gargs, ('GET', url), 200, headers=headers)

    url = '/api/v1/projects/%s/wifi_slices/%u' % (project_id, slice_id)
    _, slc = command.connect(gargs, ('GET', url), 200, headers=headers)

    accum = []

    accum.append("project id ")
    accum.append(prj['project_id'])
    accum.append(" SSID ")

    if 'wifi_props' not in prj or not prj['wifi_props']:
        accum.append("UNDEFINED")
    else:
        accum.append(prj['wifi_props']['ssid'])

    accum.append("\nSlice ID: ")
    accum.append(str(slc['slice_id']))

    for k, val in slc['properties'].items():
        accum.append("\n    %s: %s" % (k, val))

    print(''.join(accum))


def pa_delete_wifi_slice(args, cmd):
    """Delete wifi slice parser method. """

    usage = "%s <project_id> <slice_id>" % command.USAGE.format(cmd)
    desc = command.DESCS[cmd]
    (args, leftovers) = \
        argparse.ArgumentParser(usage=usage,
                                description=desc).parse_known_args(args)
    return args, leftovers


def do_delete_wifi_slice(gargs, args, leftovers):
    """Delete wifi slice. """

    if len(leftovers) != 2:
        print("Invalid parameter, run help load-delete-wifi-slice")
        command.print_available_cmds()
        sys.exit()

    project_id = uuid.UUID(leftovers[0])
    slice_id = int(leftovers[1])

    url = '/api/v1/projects/%s/wifi_slices/%u' % (project_id, slice_id)
    command.connect(gargs, ('DELETE', url), 204)

    print("slice id %u status DELETED" % slice_id)
