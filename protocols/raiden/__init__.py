# -*- coding: utf-8 -*-

"""
This module contains the support resources for the raiden protocol.

It was created with protocol buffer compiler version `libprotoc 3.19.4` and aea version `1.2.0`.
"""

from packages.brainbot.protocols.raiden.message import RaidenMessage
from packages.brainbot.protocols.raiden.serialization import RaidenSerializer


RaidenMessage.serializer = RaidenSerializer
