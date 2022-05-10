import requests
from datetime import datetime, timedelta

URL = "https://qbittorrent/api/v2/"
SID = "" # SID can be found in your qBittorrent cookies
WEEKS = 2

COOKIES = {"SID": SID}

if (URL[-1] != "/"):
    URL += "/"

response = requests.get(URL + "sync/maindata", cookies = COOKIES)

torrents = response.json()["torrents"]

for torrent in torrents:
    torrent_data = torrents[torrent]
    added_on = datetime.fromtimestamp(torrent_data["added_on"])
    week_delta = timedelta(weeks=WEEKS)
    if (added_on + week_delta < datetime.now()):
        print(str(datetime.now()) + " --- [INFO] DELETE TORRENT " + torrent_data["name"])
        req_data = {"hashes": torrent, "deleteFiles": "true"}
        requests.post(URL + "torrents/delete", data=req_data, cookies=COOKIES)