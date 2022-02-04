# SUMMONER-V4

import pandas as pd
import requests
import time


def getsummoner(region, summonerid, api_key, retry=True):
    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/' + summonerid
    req = requests.get(url, headers={'X-Riot-Token': api_key})
    if retry and req.status_code == 429:
        time.sleep(int(req.headers['Retry-After']))
        req = requests.get(url, headers={'X-Riot-Token': api_key})
    return pd.Series(req.json())
