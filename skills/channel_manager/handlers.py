from typing import Optional, cast

from aea.configurations.base import PublicId
from aea.protocols.base import Message
from aea.skills.base import Handler
from packages.brainbot.protocols.raiden.message import RaidenMessage
import raiden_api_client

raiden = raiden_api_client.RaidenAPIWrapper(ip="127.0.0.1", port="5001")


class ChannelHandler(Handler):
    """This class handles operations in channels."""

    SUPPORTED_PROTOCOL = RaidenMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """Implement the setup."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        handlers = {
            RaidenMessage.Performative.STOP_NODE: self.stop_node,
            RaidenMessage.Performative.OPEN_CHANNEL: self.open_channel,
            RaidenMessage.Performative.CLOSE_CHANNEL: self.close_channel,
            RaidenMessage.Performative.TRANSFER: self.transfer,
            RaidenMessage.Performative.DEPOSIT: self.deposit
        }
        raiden_message_type = message.performative
        handler = handlers.get(raiden_message_type)
        if not handler:
            raise NotImplemented(f"No handler for message type {raiden_message_type}")
        message = cast(RaidenMessage, message)
        handler(message)

    def stop_node(self, **kwargs) -> None:
        self.context.logger.info(f"Received message stop_node")
        self.teardown()

    def open_channel(self, message: RaidenMessage) -> None:
        self.send_raiden_message("open_channel", message, message.partner_address, message.token_address, message.amount)
        
    def close_channel(self, message: RaidenMessage) -> None:
        self.send_raiden_message("close_channel", message, message.partner_address, message.token_address)
        
    def transfer(self, message: RaidenMessage) -> None:
        self.send_raiden_message("transfer", message, message.partner_address, message.token_address, message.amount)
        

    def deposit(self, message: RaidenMessage) -> None:
        self.send_raiden_message("fund_channel", message, message.partner_address, message.token_address, message.amount)

    def send_raiden_message(self, method, message, *args, **kwargs):
        try:
            response = getattr(raiden, method)(*args, **kwargs)
            response = message.reply(
                performative=RaidenMessage.Performative.SUCCESS,
                action=message.performative,
                detail=response,
            )
        except Exception as e:
            response = message.reply(
                performative=RaidenMessage.Performative.FAILURE,
                action=message.performative,
                detail=str(e),
            )
        self.context.logger.info(f"{method}: {response}")
        self.context.outbox.put_message(response)
        return response

    def teardown(self) -> None:
        pass

