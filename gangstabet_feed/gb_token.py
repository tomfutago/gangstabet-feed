import os
import json
from gangstabet_feed import icx_tx
from dotenv import load_dotenv

# load env variables
is_heroku = os.getenv("IS_HEROKU", None)
if not is_heroku:
    load_dotenv()

class GBToken:
    def __init__(self, txInfo: icx_tx.TxInfo, tokenInfo: json) -> None:
        # obfuscate address
        self.address = txInfo.address[:8] + ".." + txInfo.address[34:]
        
        # get common attributes
        self.id = int(tokenInfo["id"])
        self.name = str(tokenInfo["name"])
        self.index = int(tokenInfo["index"])
        self.type = str(tokenInfo["type"])
        self.class_name = str(tokenInfo["class"])
        self.image_url = tokenInfo["image_url"]
        self.external_url = "https://gangstabet.io/profile/" + str(tokenInfo["id"])
        self.timestamp = txInfo.timestamp
        self.info = "\n"

        # set destination discord channel
        if txInfo.method == "set_nft_characters":
            self.discord_webhook = os.getenv("DISCORD_MARKET_WEBHOOK")
        else:
            self.discord_webhook = os.getenv("DISCORD_LOG_WEBHOOK")

        # collect building blocks for discord embed
        if txInfo.method == "set_nft_characters":
            self.title = "GangstaBet created!"
            self.footer = "Created on "
            self.info += "\nHappy owner: " + self.address
        
        self.info += "\n[Check it out](" + self.external_url + ")"

        # todo: attributes - it's dictionary, not list
        #attributesList = []
        #for attribute in tokenInfo["attributes"]:
        #    attributesList.append(str(attribute["name"]))
        #self.attributes = ', '.join(attributesList)

        # todo: additionalCounterpart

    def generate_discord_info(self) -> str:
        # create discord info output
        # markdown options: *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`
        info = "**" + self.name + "**"
        info += "\n" + self.type + " / " + self.class_name

        #if len(self.attributes) > 0:
        #    info += "\nAttributes: " + self.attributes
        
        info += self.info
        return info

    def set_color(self) -> str:
        type = self.type
        color = "808B96" #default: gray
        if type == "Gangster":
            color = "E74C3C" #red
        elif type == "Detective":
            color = "3498DB" #blue
        return color
