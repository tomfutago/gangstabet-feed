import sys
import json
import requests
from time import sleep
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.exception import JSONRPCException
from discord_webhook import DiscordWebhook, DiscordEmbed

from gangstabet_feed import icx_tx
from gangstabet_feed import gb_token

# GangstaBet contracts
GangstaBetCx = "cx384018e03aa8b739472c7a0645b70df97550e2c2"
GangstaBetSkillCx = "cx2dc662031f3d62bcdba4f63e9bf827767c847565"
GangstaBetTokenCx = "cx6139a27c15f1653471ffba0b4b88dc15de7e3267"

# connect to ICON main-net
icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

# function for making a call
def call(to, method, params):
    call = CallBuilder().to(to).method(method).params(params).build()
    result = icon_service.call(call)
    return result


# latest block height
#block_height = icon_service.get_block("latest")["height"]

#block_height = 40806971
#block_height = 40806977
#block_height = 40731695 # failure
#block = icon_service.get_block(block_height)
#print(json.dumps(block, indent = 4))
#txHash = "0xfad47e254414893ab812cdc46968178cb6456cd9a45163e256c260a0dd4eb95e"
#txResult = icon_service.get_transaction_result(txHash)
#print(txResult)

block_height = 40731481 # start block with first claimed GBs

while True:
    try:
        block = icon_service.get_block(block_height)
        #print("block:", block_height)
    except JSONRPCException:
        sleep(2)
        continue
    else:
        try:
            for tx in block["confirmed_transaction_list"]:
                if "to" in tx:
                    if tx["to"] == GangstaBetCx:
                        try:
                            # check if tx uses expected method - if not skip and move on
                            method = tx["data"]["method"]
                            #print("block:", block_height, "method:", method, "processing..")

                            expected_methods = ["set_nft_characters"]
                            if method not in expected_methods:
                                continue

                            # create instance of current transaction
                            txInfoCurrent = icx_tx.TxInfo(tx)

                            # check if tx was successful - if not skip and move on
                            txResult = icon_service.get_transaction_result(txInfoCurrent.txHash)
                            # status : 1 on success, 0 on failure
                            if txResult["status"] == 0:
                                continue
                            
                            # pull token details - if gb_id cannot be retrieved (-1) skip and move on
                            if txInfoCurrent.get_gb_id() == -1:
                                #todo: send to log webhook
                                continue
                            tokenInfo = requests.get(txInfoCurrent.get_gb_apiurl()).json()
                            tokenCharacterInfo = call(txInfoCurrent.contract, "get_character_info", {"nft_id": txInfoCurrent.get_gb_id()})

                            # check if json ok - if not skip and move on
                            if "error" in tokenInfo:
                                #todo: send to log webhook
                                print("token info contains 'error'..")
                                continue

                            # get token info
                            token = gb_token.GBToken(txInfoCurrent, tokenInfo)

                            if len(token.info) > 0:
                                sleep(2)
                                webhook = DiscordWebhook(url=token.discord_webhook)
                                embed = DiscordEmbed(title=token.title, description=token.generate_discord_info(), color=token.set_color())
                                embed.set_thumbnail(url=token.image_url)
                                embed.set_footer(text=token.footer)
                                embed.set_timestamp(token.timestamp)
                                webhook.add_embed(embed)
                                response = webhook.execute()
                        except:
                            print("Error: {}. {}, line: {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
                            continue

            block_height += 1
        except:
            sleep(2)
            continue
