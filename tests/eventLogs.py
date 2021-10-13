from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

GangstaBetTokenCx = "cx6139a27c15f1653471ffba0b4b88dc15de7e3267"

# connect to ICON main-net
icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

# util function
def hex_to_int(hex) -> int:
    return int(hex, 16)

txHash = "0xf714c23e791432bfd1e65e109267eca4ba3ec0b420c8d83965720a23cfeca888"
txResult = icon_service.get_transaction_result(txHash)
for x in txResult["eventLogs"]:
    if x["scoreAddress"] == GangstaBetTokenCx:
        if "Transfer(Address,Address,int,bytes)" in x["indexed"]:
            print(hex_to_int(x["indexed"][3]) / 10 ** 18)
