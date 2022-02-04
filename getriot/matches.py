# MATCH-V5

import pandas as pd
import requests
import time


def getmatches(region, puuid, api_key, starttime=None, endtime=None, queue=None, type=None, start=0, count=20, retry=True):
    url = 'https://' + region + '.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid + '/ids?'
    if starttime is not None:
        url += 'startTime=' + str(starttime)
    if endtime is not None:
        url += '&endTime=' + str(endtime)
    if queue is not None:
        url += '&queue=' + str(queue)
    if type is not None:
        url += '&type=' + type
    url += '&start=' + str(start) + '&count=' + str(count)
    req = requests.get(url, headers={'X-Riot-Token': api_key})
    if retry and req.status_code == 429:
        time.sleep(int(req.headers['Retry-After']))
        req = requests.get(url, headers={'X-Riot-Token': api_key})
    return pd.Series(req.json())
