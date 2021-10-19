import re
import json
from datetime import datetime
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.exception import JSONRPCException

# GangstaBet contracts
GangstaBetCx = "cx384018e03aa8b739472c7a0645b70df97550e2c2"
GangstaBetSkillCx = "cx2dc662031f3d62bcdba4f63e9bf827767c847565"
GangstaBetTokenCx = "cx6139a27c15f1653471ffba0b4b88dc15de7e3267"
GangstaBetMarketCx = "cx8683d50b9f53275081e13b64fba9d6a56b7c575d"

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
        self.contract = GangstaBetCx #str(tx["to"])
        self.address = str(tx["from"])
        #self.timestamp = datetime.fromtimestamp(tx["timestamp"] / 1000000).replace(microsecond=0).isoformat()
        self.timestamp = int(tx["timestamp"] / 1000000)
        #self.cost = "{:.2f}".format(int(tx["value"]) / 10 ** 18) #n/a for set_nft_characters
        self.method = tx["data"]["method"]

        if self.method == "set_nft_characters":
            self.cost = str("80.00 ICX") #flat initial fee
            self.nft_info = str(tx["data"]["params"]["nft_info"])
            self.nft_id = self.get_gb_id()
            self.nft_update = str("")
        elif self.method == "change_name":
            self.cost = self.get_transfer_gbet()
            self.nft_info = str("")
            self.nft_id = hex_to_int(tx["data"]["params"]["nft_id"])
            self.nft_update = str(tx["data"]["params"]["nft_name"])
        elif self.method == "claim_allocated_amt":
            self.cost = self.get_transfer_gbet()
            self.nft_info = str("")
            self.nft_id = hex_to_int(tx["data"]["params"]["nft_id"])
            self.nft_update = str("")
        elif self.method == "increase_status_level":
            self.cost = self.get_transfer_gbet()
            self.nft_info = str("")
            self.nft_id = int(tx["data"]["params"]["nft_id"])
            self.nft_update = str(tx["data"]["params"]["skill_inc_mapping"])
        elif self.method == "set_price":
            self.cost = "{:.2f}".format(int(tx["data"]["params"]["nft_info"]) / 10 ** 18) + " ICX"
            self.nft_info = str("")
            self.nft_id = hex_to_int(tx["data"]["params"]["nft_id"])
            self.nft_update = str("")
        elif self.method == "buy":
            self.cost = "{:.2f}".format(int(tx["value"]) / 10 ** 18) + " ICX"
            self.nft_info = str("")
            self.nft_id = hex_to_int(tx["data"]["params"]["nft_id"])
            self.nft_update = str("")


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
            gb_apiurl = ""
        return gb_apiurl

    def get_transfer_gbet(self) -> str:
        txResult = icon_service.get_transaction_result(self.txHash)
        gbet_amt = ""
        if txResult["status"] == 1: #success
            for x in txResult["eventLogs"]:
                if x["scoreAddress"] == GangstaBetTokenCx:
                    if "Transfer(Address,Address,int,bytes)" in x["indexed"]:
                        gbet_amt = str(hex_to_int(x["indexed"][3]) / 10 ** 18) + " GBET"
        return gbet_amt
