# -*- coding: utf-8 -*-

"""This module contains raiden's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Optional, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message


_default_logger = logging.getLogger("aea.packages.brainbot.protocols.raiden.message")

DEFAULT_BODY_SIZE = 4


class RaidenMessage(Message):
    """Autonomous implementation of the Raiden protocol"""

    protocol_id = PublicId.from_str("brainbot/raiden:0.0.1")
    protocol_specification_id = PublicId.from_str("brainbot/raiden:0.0.1")

    class Performative(Message.Performative):
        """Performatives for the raiden protocol."""

        CLOSE_CHANNEL = "close_channel"
        DEPOSIT = "deposit"
        FAILURE = "failure"
        OPEN_CHANNEL = "open_channel"
        STOP_NODE = "stop_node"
        SUCCESS = "success"
        TRANSFER = "transfer"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "close_channel",
        "deposit",
        "failure",
        "open_channel",
        "stop_node",
        "success",
        "transfer",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "action",
            "amount",
            "detail",
            "dialogue_reference",
            "message_id",
            "partner_address",
            "performative",
            "target",
            "token_address",
            "total_deposit",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of RaidenMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        :param **kwargs: extra options.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=RaidenMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(RaidenMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def action(self) -> str:
        """Get the 'action' content from the message."""
        enforce(self.is_set("action"), "'action' content is not set.")
        return cast(str, self.get("action"))

    @property
    def amount(self) -> str:
        """Get the 'amount' content from the message."""
        enforce(self.is_set("amount"), "'amount' content is not set.")
        return cast(str, self.get("amount"))

    @property
    def detail(self) -> Optional[str]:
        """Get the 'detail' content from the message."""
        return cast(Optional[str], self.get("detail"))

    @property
    def partner_address(self) -> str:
        """Get the 'partner_address' content from the message."""
        enforce(self.is_set("partner_address"), "'partner_address' content is not set.")
        return cast(str, self.get("partner_address"))

    @property
    def token_address(self) -> str:
        """Get the 'token_address' content from the message."""
        enforce(self.is_set("token_address"), "'token_address' content is not set.")
        return cast(str, self.get("token_address"))

    @property
    def total_deposit(self) -> str:
        """Get the 'total_deposit' content from the message."""
        enforce(self.is_set("total_deposit"), "'total_deposit' content is not set.")
        return cast(str, self.get("total_deposit"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the raiden protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                    type(self.message_id)
                ),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                    type(self.target)
                ),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, RaidenMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == RaidenMessage.Performative.OPEN_CHANNEL:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.partner_address, str),
                    "Invalid type for content 'partner_address'. Expected 'str'. Found '{}'.".format(
                        type(self.partner_address)
                    ),
                )
                enforce(
                    isinstance(self.token_address, str),
                    "Invalid type for content 'token_address'. Expected 'str'. Found '{}'.".format(
                        type(self.token_address)
                    ),
                )
                enforce(
                    isinstance(self.total_deposit, str),
                    "Invalid type for content 'total_deposit'. Expected 'str'. Found '{}'.".format(
                        type(self.total_deposit)
                    ),
                )
            elif self.performative == RaidenMessage.Performative.CLOSE_CHANNEL:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.partner_address, str),
                    "Invalid type for content 'partner_address'. Expected 'str'. Found '{}'.".format(
                        type(self.partner_address)
                    ),
                )
                enforce(
                    isinstance(self.token_address, str),
                    "Invalid type for content 'token_address'. Expected 'str'. Found '{}'.".format(
                        type(self.token_address)
                    ),
                )
            elif self.performative == RaidenMessage.Performative.DEPOSIT:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.partner_address, str),
                    "Invalid type for content 'partner_address'. Expected 'str'. Found '{}'.".format(
                        type(self.partner_address)
                    ),
                )
                enforce(
                    isinstance(self.token_address, str),
                    "Invalid type for content 'token_address'. Expected 'str'. Found '{}'.".format(
                        type(self.token_address)
                    ),
                )
                enforce(
                    isinstance(self.amount, str),
                    "Invalid type for content 'amount'. Expected 'str'. Found '{}'.".format(
                        type(self.amount)
                    ),
                )
            elif self.performative == RaidenMessage.Performative.TRANSFER:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.partner_address, str),
                    "Invalid type for content 'partner_address'. Expected 'str'. Found '{}'.".format(
                        type(self.partner_address)
                    ),
                )
                enforce(
                    isinstance(self.token_address, str),
                    "Invalid type for content 'token_address'. Expected 'str'. Found '{}'.".format(
                        type(self.token_address)
                    ),
                )
                enforce(
                    isinstance(self.amount, str),
                    "Invalid type for content 'amount'. Expected 'str'. Found '{}'.".format(
                        type(self.amount)
                    ),
                )
            elif self.performative == RaidenMessage.Performative.SUCCESS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.action, str),
                    "Invalid type for content 'action'. Expected 'str'. Found '{}'.".format(
                        type(self.action)
                    ),
                )
                if self.is_set("detail"):
                    expected_nb_of_contents += 1
                    detail = cast(str, self.detail)
                    enforce(
                        isinstance(detail, str),
                        "Invalid type for content 'detail'. Expected 'str'. Found '{}'.".format(
                            type(detail)
                        ),
                    )
            elif self.performative == RaidenMessage.Performative.FAILURE:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.action, str),
                    "Invalid type for content 'action'. Expected 'str'. Found '{}'.".format(
                        type(self.action)
                    ),
                )
                if self.is_set("detail"):
                    expected_nb_of_contents += 1
                    detail = cast(str, self.detail)
                    enforce(
                        isinstance(detail, str),
                        "Invalid type for content 'detail'. Expected 'str'. Found '{}'.".format(
                            type(detail)
                        ),
                    )
            elif self.performative == RaidenMessage.Performative.STOP_NODE:
                expected_nb_of_contents = 0

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                        self.target
                    ),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
