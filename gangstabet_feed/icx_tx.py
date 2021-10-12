import re
import json
from datetime import datetime
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.exception import JSONRPCException

# connect to ICON main-net
icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

# util function
def hex_to_int(hex) -> int:
    return int(hex, 16)

# not used atm..
class IcxBlock:
    def __init__(self) -> None:
        self.block_height = icon_service.get_block("latest")["height"]
        self.block = icon_service.get_block(self.block_height)

    def get_latest_block(self) -> dict:
        return icon_service.get_block("latest")

    def get_block(self, block: int) -> dict:
        return icon_service.get_block(block)
        
    def get_tx_result(self, tx_hash: str) -> dict:
        return icon_service.get_transaction_result(tx_hash)

    def call(self, to, method, params=None):
        try:
            call = CallBuilder().to(to).method(method).params(params).build()
            result = icon_service.call(call)
            return result
        except JSONRPCException as e:
            raise Exception(e)

# class to collect info available in icx transaction
class TxInfo:
    def __init__(self, tx: json) -> None:
        self.txHash = str(tx["txHash"])
        self.contract = str(tx["to"])
        self.address = str(tx["from"])
        #self.timestamp = datetime.fromtimestamp(tx["timestamp"] / 1000000).replace(microsecond=0).isoformat()
        self.timestamp = int(tx["timestamp"] / 1000000)
        self.method = tx["data"]["method"]

        if self.method == "request_character_creation":
            self.cost = "{:.2f}".format(int(tx["value"]) / 10 ** 18)
            self.nft_count = int(tx["data"]["params"]["nft_count"])
            self.nft_info = str("")
        elif self.method == "set_nft_characters":
            self.cost = str("")
            self.nft_count = int(-1)
            self.nft_info = str(tx["data"]["params"]["nft_info"])

    def get_gb_id(self) -> int:
        found = re.search('{\"(.+?)\":', self.nft_info)
        if found:
            gb_id = found.group(1)
        else:
            gb_id = -1
        return gb_id

    def get_gb_apiurl(self) -> str:
        found = re.search('\",\"(.+?)\"]}', self.nft_info)
        if found:
            gb_apiurl = found.group(1)
        else:
            gb_apiurl = -1
        return gb_apiurl
