# -*- coding: utf-8 -*-

"""
This module contains the classes required for raiden dialogue management.

- RaidenDialogue: The dialogue class maintains state of a dialogue and manages it.
- RaidenDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, Dict, FrozenSet, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues

from packages.brainbot.protocols.raiden.message import RaidenMessage


class RaidenDialogue(Dialogue):
    """The raiden dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {
            RaidenMessage.Performative.OPEN_CHANNEL,
            RaidenMessage.Performative.CLOSE_CHANNEL,
            RaidenMessage.Performative.DEPOSIT,
            RaidenMessage.Performative.TRANSFER,
        }
    )
    TERMINAL_PERFORMATIVES: FrozenSet[Message.Performative] = frozenset(
        {RaidenMessage.Performative.SUCCESS, RaidenMessage.Performative.FAILURE}
    )
    VALID_REPLIES: Dict[Message.Performative, FrozenSet[Message.Performative]] = {
        RaidenMessage.Performative.CLOSE_CHANNEL: frozenset(
            {RaidenMessage.Performative.SUCCESS, RaidenMessage.Performative.FAILURE}
        ),
        RaidenMessage.Performative.DEPOSIT: frozenset(
            {RaidenMessage.Performative.SUCCESS, RaidenMessage.Performative.FAILURE}
        ),
        RaidenMessage.Performative.FAILURE: frozenset(),
        RaidenMessage.Performative.OPEN_CHANNEL: frozenset(
            {RaidenMessage.Performative.SUCCESS, RaidenMessage.Performative.FAILURE}
        ),
        RaidenMessage.Performative.STOP_NODE: frozenset(
            {RaidenMessage.Performative.SUCCESS, RaidenMessage.Performative.FAILURE}
        ),
        RaidenMessage.Performative.SUCCESS: frozenset(),
        RaidenMessage.Performative.TRANSFER: frozenset(
            {RaidenMessage.Performative.SUCCESS, RaidenMessage.Performative.FAILURE}
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a raiden dialogue."""

        NODE = "node"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a raiden dialogue."""

        SUCCESS = 0
        FAILURE = 1

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[RaidenMessage] = RaidenMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :param message_class: the message class used
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class RaidenDialogues(Dialogues, ABC):
    """This class keeps track of all raiden dialogues."""

    END_STATES = frozenset(
        {RaidenDialogue.EndState.SUCCESS, RaidenDialogue.EndState.FAILURE}
    )

    _keep_terminal_state_dialogues = True

    def __init__(
        self,
        self_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[RaidenDialogue] = RaidenDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param self_address: the address of the entity for whom dialogues are maintained
        :param dialogue_class: the dialogue class used
        :param role_from_first_message: the callable determining role from first message
        """
        Dialogues.__init__(
            self,
            self_address=self_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=RaidenMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
