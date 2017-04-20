#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing tests for the Thorlabs TC200
"""

# IMPORTS ####################################################################

from __future__ import absolute_import

from nose.tools import raises
import quantities as pq
import struct

import instruments as ik
from instruments.thorlabs._packets import ThorLabsPacket, hw_info
from instruments.thorlabs._cmds import ThorLabsCommands
from instruments.tests import expected_protocol

# TESTS ######################################################################


def test_apt_hw_info():
    with expected_protocol(
        ik.thorlabs.ThorLabsAPT,
        [
            ThorLabsPacket(
                message_id=ThorLabsCommands.HW_REQ_INFO,
                param1=0x00, param2=0x00,
                dest=0x50,
                source=0x01,
                data=None
            ).pack()
        ],
        [
            ThorLabsPacket(
                message_id=ThorLabsCommands.HW_GET_INFO,
                dest=0x01,
                source=0x50,
                data=hw_info.pack(
                    # Serial number
                    0x1234, 
                    # Model number
                    "ABC-123".encode('ascii'), 
                    # HW type
                    3, 
                    # FW version,
                    0xa1, 0xa2, 0xa3, 
                    # Notes
                    "abcdefg".encode('ascii'),
                    # HW version
                    42,
                    # Mod state
                    43,
                    # Number of channels
                    2
                )
            ).pack()
        ],
        sep=""
    ) as apt:
        # Check internal representations.
        # NB: we shouldn't do this in some sense, but these fields
        #     act as an API to the APT subclasses.
        assert apt._hw_type == "Unknown type: 3"
        assert apt._fw_version == "a1.a2.a3"
        assert apt._notes == "abcdefg"
        assert apt._hw_version == 42
        assert apt._mod_state == 43

        # Check external API.
        assert apt.serial_number == 0x1234
        assert apt.model_number == 'ABC-123'
        assert apt.name == "ThorLabs APT Instrument model ABC-123, serial 1234 (HW version 42, FW version a1.a2.a3)"

