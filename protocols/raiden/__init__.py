# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 brainbot
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""
This module contains the support resources for the raiden protocol.

It was created with protocol buffer compiler version `libprotoc 3.20.0` and aea version `1.1.1`.
"""

from packages.brainbot.protocols.raiden.message import RaidenMessage
from packages.brainbot.protocols.raiden.serialization import RaidenSerializer


RaidenMessage.serializer = RaidenSerializer
