import re
s = "{\"2975\":[true,\"Marksman\",\"https://api.gangstabet.io/api/index/2296\"]}"

found = re.search('{\"(.+?)\":', s)
if found:
    gb_id = found.group(1)
    print(gb_id)

found = re.search('\",\"(.+?)\"]}', s)
if found:
    gb_url = found.group(1)
    print(gb_url)
