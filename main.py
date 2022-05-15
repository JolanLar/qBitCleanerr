from email.policy import default
import requests, condition
from datetime import datetime, timedelta

URL = "https://qbittorrent/api/v2/"
USER = "" # qBittorrent username
PASSWORD = "" # qBittorrent password

# Torrent is deleted after the number of days of the first condition that matches
# If no one match, take DEFAULT DAYS (None = never)

# Here, if magnet contain 'nyaa', the torrent is deleted immediately, else it will be deleted after 30 days
CONDITIONS = [condition.Condition("magnet_uri", "nyaa", 0)]
DEFAULT_DAYS = 30


login_data = {
    "username": USER,
    "password": PASSWORD
}

def log(level, message):
    print(datetime.now().strftime('%d-%m-%Y, %H:%M:%S') + " --- [" + str(level) + "] " + str(message))

def check_conditions(torrent_data):
    if torrent_data["progress"] == 1:
        for CONDITION in CONDITIONS:
            if CONDITION.included_value in torrent_data[CONDITION.id]:
                return CONDITION.days
        return DEFAULT_DAYS
    else:
        return None


log("INFO", "Job start !")

session = requests.Session()
session.post(URL + "auth/login", login_data)

if (URL[-1] != "/"):
    URL += "/"

response = session.get(URL + "sync/maindata")
torrents = response.json()["torrents"]

for torrent in torrents:
    torrent_data = torrents[torrent]
    days = check_conditions(torrent_data)
    if days != None:
        added_on = datetime.fromtimestamp(torrent_data["added_on"])
        days_delta = timedelta(days=days)
        if added_on + days_delta < datetime.now():
            log("INFO", "DELETE TORRENT " + torrent_data["name"])
            req_data = {"hashes": torrent, "deleteFiles": "true"}
            session.post(URL + "torrents/delete", data=req_data)

log("INFO", "Job end !")