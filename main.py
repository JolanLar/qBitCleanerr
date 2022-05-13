from email.policy import default
import requests, condition
from datetime import datetime, timedelta

URL = "https://qbittorrent/api/v2/"
SID = "" # SID can be found in your qBittorrent cookies
CONDITIONS = [condition.Condition("magnet_uri", "nyaa", 0), condition.Condition("default", "", 60)]


COOKIES = {"SID": SID}

if (URL[-1] != "/"):
    URL += "/"

def check_conditions(torrent_data):
    if torrent_data["progress"] == 1:
        for CONDITION in CONDITIONS:
            if CONDITION.id == "default":
                return CONDITION.days
            elif CONDITION.included_value in torrent_data[CONDITION.id]:
                return CONDITION.days
    return None

print(datetime.now().strftime('%d-%m-%Y, %H:%M:%S') + " --- [INFO] Job start !")

response = requests.get(URL + "sync/maindata", cookies = COOKIES)
torrents = response.json()["torrents"]

for torrent in torrents:
    torrent_data = torrents[torrent]
    days = check_conditions(torrent_data)
    if days != None:
        added_on = datetime.fromtimestamp(torrent_data["added_on"])
        days_delta = timedelta(days=days)
        if added_on + days_delta < datetime.now():
            print(datetime.now().strftime('%d-%m-%Y, %H:%M:%S') + " --- [INFO] DELETE TORRENT " + torrent_data["name"])
            req_data = {"hashes": torrent, "deleteFiles": "true"}
            requests.post(URL + "torrents/delete", data=req_data, cookies=COOKIES)

            
print(datetime.now().strftime('%d-%m-%Y, %H:%M:%S') + " --- [INFO] Job end !")