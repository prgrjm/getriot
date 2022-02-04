import pandas
import pandas as pd
import getriot

api_key = 'RGAPI-ed520406-4425-4e3a-b48d-195ada86b236'

var = False  # 챌린저, 그마, 마스터의 정보를 저장
if var:
    df0 = getriot.gethighleagues('kr', 'c', 'solo', api_key)
    df1 = getriot.gethighleagues('kr', 'gm', 'solo', api_key)
    df2 = getriot.gethighleagues('kr', 'm', 'solo', api_key)
    df3 = pd.concat([df0, df1, df2])
    df3.to_csv('highleagues.csv', index=False)

var = False  # 위에 있는 챌그마마 정보에 있는 summonerid를 토대로 해당 소환사 목록에 추가될 정보를 저장
if var:
    highleagues = pd.read_csv('highleagues.csv')
    summonerids = highleagues['summonerId']
    s0 = getriot.getsummoner('kr', summonerids[0], api_key)
    highsummoners = s0.to_frame().T
    for i, summonerid in enumerate(summonerids[1:]):
        s1 = getriot.getsummoner('kr', summonerid, api_key)
        highsummoners = pd.concat([highsummoners, s1.to_frame().T], ignore_index=True)
        if not (i + 1) % 100:
            highsummoners.to_csv('highsummoners.csv', index=False)
            print(i + 1)
    highsummoners.to_csv('highsummoners.csv', index=False)

var = False  # 위에 있는 두 정보를 합쳐서 저장
if var:
    highleagues = pd.read_csv('highleagues.csv')
    highsummoners = pd.read_csv('highsummoners.csv')
    advancedhighleagues = pd.concat([highleagues, highsummoners.drop(['id', 'name'], axis=1)], axis=1)
    advancedhighleagues.to_csv('advancedhighleagues.csv', index=False)

var = True
if var:
    advancedhighleagues = pd.read_csv('advancedhighleagues.csv')
    highmatches = set()
    df0 = advancedhighleagues[['wins', 'losses', 'puuid']]
    for index, wins, losses, puuid in df0.itertuples():
        highmatches |= set(getriot.getmatches('asia', puuid, api_key, queue=420, count=100 if wins + losses > 100 else wins + losses))
        if not index % 100:
            pandas.DataFrame(highmatches).to_csv('highmatches.csv', index=False)
            print(index)
    pandas.DataFrame(highmatches).to_csv('highmatches.csv', index=False)
