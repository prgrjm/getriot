# LEAGUE-V4

import pandas as pd
import requests
import time


def gethighleagues(region, tier, queue, api_key, retry=True):
    t_dict = {'c': 'challenger', 'gm': 'grandmaster', 'm': 'master'}
    if tier in t_dict:
        tier = t_dict[tier]
    q_dict = {'solo': 'RANKED_SOLO_5x5', 'flex': 'RANKED_FLEX_SR'}
    if queue in q_dict:
        queue = q_dict[queue]

    url = 'https://' + region + '.api.riotgames.com/lol/league/v4/' + tier + 'leagues/by-queue/' + queue
    req = requests.get(url, headers={'X-Riot-Token': api_key})
    if retry and req.status_code == 429:
        time.sleep(int(req.headers['Retry-After']))
        req = requests.get(url, headers={'X-Riot-Token': api_key})

    df0 = pd.DataFrame(req.json())
    df1 = pd.DataFrame(dict(df0.pop('entries'))).T
    return pd.concat([df0, df1], axis=1)
