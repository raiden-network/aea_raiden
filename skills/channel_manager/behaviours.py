import subprocess
import secrets
from os.path import exists
from time import sleep
from typing import cast
from aea.skills.behaviours import TickerBehaviour
import raiden_api_client

raiden = raiden_api_client.RaidenAPIWrapper(ip="127.0.0.1", port="5001")

CHANNEL_CHECK_INTERVAL = 60.0  # time in seconds
DEFAULT_NETWORK = "5"
DEFAULT_KEYSTORE = "/usr/lib/raiden/keystore"
DEFAULT_KEYSTORE_PASSWORD = "/usr/lib/raiden/password"


class ChannelMonitorBehaviour(TickerBehaviour):
    """This class spins up a Raiden Node and monitors channels."""
    account_address_path = "/usr/lib/raiden/address"

    def __init__(self, **kwargs):
        """Initialize the monitor behaviour."""
        monitor_interval = cast(
            float, kwargs.pop("channel_check_interval", CHANNEL_CHECK_INTERVAL)
        )

        self.keystore_path = kwargs.pop("keystore_path", DEFAULT_KEYSTORE)
        self.password_file = kwargs.pop("password_file", DEFAULT_KEYSTORE_PASSWORD)
        if not exists(self.password_file) or not exists(self.keystore_path):
            self.__create_account()
        else:
            self.address = open(self.account_address_path, "r").read()

        self.network_id = kwargs.pop("network_id", DEFAULT_NETWORK)
        self.rpc_endpoint = self.__parse_rpc_endpoint(kwargs.pop("rpc_endpoint", ""), kwargs.pop("infura_id", ""))

        super().__init__(tick_interval=monitor_interval, **kwargs)


    def __parse_rpc_endpoint(self, endpoint: str, infura_id: str) -> str:
        """Parse the RPC endpoint."""
        if not endpoint and not infura_id:
            raise RuntimeError("RPC endpoint is not specified")
        return endpoint or f"{self.__choose_infura_endpoint()}/{infura_id}"

    def __choose_infura_endpoint(self) -> str:
        """Choose the Infura endpoint."""
        infura_choices = {
            "mainnet": "mainnet",
            "1": "mainnet",
            "3": "ropsten",
            "4": "rinkeby",
            "goerli": "goerli",
            "5": "goerli",
        }
        network = infura_choices.get(self.network_id, None)
        if not network:
            raise RuntimeError(f"Unsupported network id {self.network_id}")
        return f"https://{network}.infura.io/v3"

    def __create_account(self) -> None:
        password_file = open(self.password_file, "w")
        password = secrets.token_hex(32)
        password_file.write(password)
        password_file.close()

        geth_result = subprocess.run(["geth", "--keystore", self.keystore_path, "--password", self.password_file, "account", "new"], capture_output=True)
        if geth_result.returncode != 0:
            raise RuntimeError(f"Failed to create account {geth_result.stderr}")
        
        self.address = geth_result.stdout.decode("utf-8").split("\n")[3].split(" ")[-1]
        open(self.account_address_path, "w+").write(self.address)


    def setup(self) -> None:
        """Implement the setup."""
        self.raiden_instance = subprocess.Popen(
            [
                "raiden",
                "--accept-disclaimer",
                "--gas-price", "fast",
                "--sync-check",
                "--log-json",
                "--log-file", "/var/log/raiden.log",
                "--development-environment", "unstable",
                "--environment-type", "development",
                "--network-id", self.network_id,
                "--eth-rpc-endpoint", self.rpc_endpoint,
                "--keystore-path", self.keystore_path,
                "--password-file", self.password_file,
                "--address", self.address,
            ]
        )
        response = {}
        tries = 0
        max_tries = 10
        while response.get("status") != "ready" and tries < max_tries:
            try:
                response = raiden.get_node_status()
                self.context.logger.info(response)
            except Exception as e:
                pass
            tries += 1
            sleep(5)
        if tries == max_tries:
            raise RuntimeError("Failed to start Raiden")

    def act(self) -> None:
        """Implement the act."""
        try:
            response = raiden.get_node_status()
            self.context.logger.info(response)
        except Exception as e:
            self.context.logger.error(e)
            self.teardown()
            self.context.logger.info("Restarting Raiden")
            self.setup()

    def teardown(self) -> None:
        """Implement the task teardown."""
        self.raiden_instance.kill()
        print("Channel monitor behaviour teardown")
