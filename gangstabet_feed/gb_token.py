import os
import json
from dotenv import load_dotenv

from gangstabet_feed import icx_tx

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
        self.nft_update = txInfo.nft_update
        self.image_url = tokenInfo["image_url"]
        self.external_url = "https://gangstabet.io/profile/" + str(tokenInfo["id"])
        self.timestamp = txInfo.timestamp
        self.info = "\n"

        # set destination discord channel
        if txInfo.method == "set_nft_characters":
            self.discord_webhook = os.getenv("DISCORD_MARKET_WEBHOOK")
        elif txInfo.method == "claim_allocated_amt" or txInfo.method == "change_name" or txInfo.method == "increase_status_level":
            self.discord_webhook = os.getenv("DISCORD_SKILLS_WEBHOOK")
        else:
            self.discord_webhook = os.getenv("DISCORD_LOG_WEBHOOK")

        # collect building blocks for discord embed
        if txInfo.method == "set_nft_characters":
            self.title = "GangstaBet created!"
            self.footer = "Created on "
            self.info += "\nHappy owner: " + self.address
            self.info += "\nPrice: " + txInfo.cost
        elif txInfo.method == "claim_allocated_amt":
            self.title = "GBET tokens claimed!"
            self.footer = "Claimed on "
            self.info += "\nAddress: " + self.address
            self.info += "\nClaimed: " + txInfo.get_transfer_gbet()
        elif txInfo.method == "change_name":
            self.title = "GangstaBet name changed!"
            self.footer = "Changed on "
            self.info += "\nAddress: " + self.address
            self.info += "\nPrice: " + txInfo.get_transfer_gbet()
        elif txInfo.method == "increase_status_level":
            self.title = "GangstaBet upgraded!"
            self.footer = "Upgraded on "
            self.info += "\nAddress: " + self.address
            self.info += "\nPrice: " + txInfo.get_transfer_gbet()
            self.info += "\n"
            self.info += "\nSkills levelled up:"
            self.info += "\n" + self.get_skills_upgrade()
        
        self.info += "\n[Check it out](" + self.external_url + ")"

        # todo: attributes - it's dictionary, not list
        #attributesList = []
        #for attribute in tokenInfo["attributes"]:
        #    attributesList.append(str(attribute["name"]))
        #self.attributes = ', '.join(attributesList)

        # todo: additionalCounterpart

    def get_skills_upgrade(self) -> str:
        s = self.nft_update.replace('{', '').replace('}', '').replace('"', '')

        if self.type == "Gangster":
            skills = ["racketeering", "shooting", "gambling", "intelligence", "strategy"]
        elif self.type == "Detective":
            skills = ["logic", "critical thinking", "incorruptible", "attention to detail", "intelligence"]

        for n in range(5):
            s = s.replace(str(n+1) + ":", skills[n] + ": ")

        skills_print_out = "\n".join(str(v) for v in s.split(","))
        return skills_print_out

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
