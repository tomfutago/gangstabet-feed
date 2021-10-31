import os
import sys
import json
import requests
from time import sleep
from dotenv import load_dotenv
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.exception import JSONRPCException
from discord_webhook import DiscordWebhook, DiscordEmbed

from gangstabet_feed import icx_tx
from gangstabet_feed import gb_token

# load env variables
is_heroku = os.getenv("IS_HEROKU", None)
if not is_heroku:
    load_dotenv()

discord_webhook = os.getenv("DISCORD_LOG_WEBHOOK")

# GangstaBet contracts
GangstaBetCx = "cx384018e03aa8b739472c7a0645b70df97550e2c2"
GangstaBetSkillCx = "cx2dc662031f3d62bcdba4f63e9bf827767c847565"
GangstaBetTokenCx = "cx6139a27c15f1653471ffba0b4b88dc15de7e3267"
GangstaBetMarketCx = "cx8683d50b9f53275081e13b64fba9d6a56b7c575d"

# connect to ICON main-net
icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

# function for making a call
def call(to, method, params):
    call = CallBuilder().to(to).method(method).params(params).build()
    result = icon_service.call(call)
    return result

# function for sending error msg to discord webhook
def send_log_to_webhook(block_height: int, txHash: str, method: str, error: str):
    err_msg = "block_height: " + str(block_height)
    err_msg += "\ntxHash: " + txHash
    err_msg += "\nmethod: " + method
    err_msg += "\nERROR: " + error
    webhook = DiscordWebhook(url=discord_webhook, rate_limit_retry=True, content=err_msg)
    response = webhook.execute()
    return response


# latest block height
block_height = icon_service.get_block("latest")["height"]

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
                    if tx["to"] == GangstaBetCx or tx["to"] == GangstaBetSkillCx or tx["to"] == GangstaBetMarketCx:
                        try:
                            # check if tx uses expected method - if not skip and move on
                            method = tx["data"]["method"]
                            #print("block:", block_height, "method:", method, "processing..")

                            expected_methods = ["set_nft_characters", "change_name", "claim_allocated_amt", "increase_status_level", "set_price", "buy"]
                            if method not in expected_methods:
                                continue

                            # create instance of current transaction
                            txInfoCurrent = icx_tx.TxInfo(tx)

                            # check if tx was successful - if not skip and move on
                            txResult = icon_service.get_transaction_result(txInfoCurrent.txHash)
                            # status : 1 on success, 0 on failure
                            if txResult["status"] == 0:
                                continue

                            tokenInfo = requests.get(call(txInfoCurrent.contract, "tokenURI", {"_id": txInfoCurrent.nft_id})).json()

                            # check if json ok - if not skip and move on
                            if "error" in tokenInfo:
                                #send to log webhook
                                response = send_log_to_webhook(block_height, tx["txHash"], method, "token info contains 'error'")
                                continue

                            # get token info
                            token = gb_token.GBToken(txInfoCurrent, tokenInfo)

                            if len(token.info) > 0:
                                # download token gif
                                #filename = "temp.gif"
                                #request = requests.get(token.image_url, stream=True)
                                #if request.status_code == 200:
                                #    with open(filename, "wb") as image:
                                #        for chunk in request:
                                #            image.write(chunk)
                                
                                # send discord msg
                                webhook = DiscordWebhook(url=token.discord_webhook, rate_limit_retry=True)
                                embed = DiscordEmbed(title=token.title, description=token.generate_discord_info(), color=token.set_color())
                                embed.set_thumbnail(url=token.image_url)
                                #embed.set_thumbnail(url="attachment://" + filename)
                                embed.set_footer(text=token.footer)
                                embed.set_timestamp(token.timestamp)
                                webhook.add_embed(embed)
                                response = webhook.execute()
                                
                                # delete temp gif
                                #os.remove(filename)
                        except:
                            #send to log webhook
                            err_msg = "{}. {}, line: {}".format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
                            response = send_log_to_webhook(block_height, tx["txHash"], method, err_msg)
                            continue

            block_height += 1
        except:
            sleep(2)
            continue
