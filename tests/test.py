from time import sleep
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))
block_height = icon_service.get_block("latest")["height"]

while True:
    block = icon_service.get_block(block_height)
    sleep(2)
    for tx in block["confirmed_transaction_list"]:
        txResult = icon_service.get_transaction_result(tx["txHash"])
        print(txResult["status"])
    block_height += 1    
