# -*- coding: utf-8 -*-

"""Serialization module for raiden protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage
from aea.mail.base_pb2 import Message as ProtobufMessage
from aea.protocols.base import Message, Serializer

from packages.brainbot.protocols.raiden import raiden_pb2
from packages.brainbot.protocols.raiden.message import RaidenMessage


class RaidenSerializer(Serializer):
    """Serialization for the 'raiden' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Raiden' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(RaidenMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        raiden_msg = raiden_pb2.RaidenMessage()

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == RaidenMessage.Performative.OPEN_CHANNEL:
            performative = raiden_pb2.RaidenMessage.Open_Channel_Performative()  # type: ignore
            partner_address = msg.partner_address
            performative.partner_address = partner_address
            token_address = msg.token_address
            performative.token_address = token_address
            total_deposit = msg.total_deposit
            performative.total_deposit = total_deposit
            raiden_msg.open_channel.CopyFrom(performative)
        elif performative_id == RaidenMessage.Performative.CLOSE_CHANNEL:
            performative = raiden_pb2.RaidenMessage.Close_Channel_Performative()  # type: ignore
            partner_address = msg.partner_address
            performative.partner_address = partner_address
            token_address = msg.token_address
            performative.token_address = token_address
            raiden_msg.close_channel.CopyFrom(performative)
        elif performative_id == RaidenMessage.Performative.DEPOSIT:
            performative = raiden_pb2.RaidenMessage.Deposit_Performative()  # type: ignore
            partner_address = msg.partner_address
            performative.partner_address = partner_address
            token_address = msg.token_address
            performative.token_address = token_address
            amount = msg.amount
            performative.amount = amount
            raiden_msg.deposit.CopyFrom(performative)
        elif performative_id == RaidenMessage.Performative.TRANSFER:
            performative = raiden_pb2.RaidenMessage.Transfer_Performative()  # type: ignore
            partner_address = msg.partner_address
            performative.partner_address = partner_address
            token_address = msg.token_address
            performative.token_address = token_address
            amount = msg.amount
            performative.amount = amount
            raiden_msg.transfer.CopyFrom(performative)
        elif performative_id == RaidenMessage.Performative.SUCCESS:
            performative = raiden_pb2.RaidenMessage.Success_Performative()  # type: ignore
            action = msg.action
            performative.action = action
            if msg.is_set("detail"):
                performative.detail_is_set = True
                detail = msg.detail
                performative.detail = detail
            raiden_msg.success.CopyFrom(performative)
        elif performative_id == RaidenMessage.Performative.FAILURE:
            performative = raiden_pb2.RaidenMessage.Failure_Performative()  # type: ignore
            action = msg.action
            performative.action = action
            if msg.is_set("detail"):
                performative.detail_is_set = True
                detail = msg.detail
                performative.detail = detail
            raiden_msg.failure.CopyFrom(performative)
        elif performative_id == RaidenMessage.Performative.STOP_NODE:
            performative = raiden_pb2.RaidenMessage.Stop_Node_Performative()  # type: ignore
            raiden_msg.stop_node.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = raiden_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Raiden' message.

        :param obj: the bytes object.
        :return: the 'Raiden' message.
        """
        message_pb = ProtobufMessage()
        raiden_pb = raiden_pb2.RaidenMessage()
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        raiden_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = raiden_pb.WhichOneof("performative")
        performative_id = RaidenMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == RaidenMessage.Performative.OPEN_CHANNEL:
            partner_address = raiden_pb.open_channel.partner_address
            performative_content["partner_address"] = partner_address
            token_address = raiden_pb.open_channel.token_address
            performative_content["token_address"] = token_address
            total_deposit = raiden_pb.open_channel.total_deposit
            performative_content["total_deposit"] = total_deposit
        elif performative_id == RaidenMessage.Performative.CLOSE_CHANNEL:
            partner_address = raiden_pb.close_channel.partner_address
            performative_content["partner_address"] = partner_address
            token_address = raiden_pb.close_channel.token_address
            performative_content["token_address"] = token_address
        elif performative_id == RaidenMessage.Performative.DEPOSIT:
            partner_address = raiden_pb.deposit.partner_address
            performative_content["partner_address"] = partner_address
            token_address = raiden_pb.deposit.token_address
            performative_content["token_address"] = token_address
            amount = raiden_pb.deposit.amount
            performative_content["amount"] = amount
        elif performative_id == RaidenMessage.Performative.TRANSFER:
            partner_address = raiden_pb.transfer.partner_address
            performative_content["partner_address"] = partner_address
            token_address = raiden_pb.transfer.token_address
            performative_content["token_address"] = token_address
            amount = raiden_pb.transfer.amount
            performative_content["amount"] = amount
        elif performative_id == RaidenMessage.Performative.SUCCESS:
            action = raiden_pb.success.action
            performative_content["action"] = action
            if raiden_pb.success.detail_is_set:
                detail = raiden_pb.success.detail
                performative_content["detail"] = detail
        elif performative_id == RaidenMessage.Performative.FAILURE:
            action = raiden_pb.failure.action
            performative_content["action"] = action
            if raiden_pb.failure.detail_is_set:
                detail = raiden_pb.failure.detail
                performative_content["detail"] = detail
        elif performative_id == RaidenMessage.Performative.STOP_NODE:
            pass
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return RaidenMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
