from riotwatcher import LolWatcher, ApiError
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.ticker as mticker
from matplotlib.pyplot import figure
from api_app.plotting.functions import largeScaleGraphTest


def damage_dealt(summoner_name, nGames, region):

    api_key = 'RGAPI-36f5d98e-4462-4c19-9078-8755d4657f18'
    watcher = LolWatcher(api_key)
    my_region = 'na1'
    me = watcher.summoner.by_name(region, summoner_name)
    # print('hello')
    # print(me)
    my_id = me['id']

    # Return the rank status for me
    my_ranked_stats = watcher.league.by_summoner(region, me['id'])
    my_matches = watcher.match.matchlist_by_account(
        my_region, me['accountId'], queue='420')

    participants = []

    for i in range(nGames):
        last_match2 = my_matches['matches'][i]
        # print(last_match2['gameId'])
        match_detail2 = watcher.match.by_id(my_region, last_match2['gameId'])
        # print(last_match2['gameId'])
        participants3 = []
        count2 = 0
        for row in match_detail2['participantIdentities']:
            participants3_row = {}
            participants3_row = row['player']['summonerId']
            participants3.append(participants3_row)
        for row in match_detail2['participants']:
            participants_row = {}
            participants_row['gameCount'] = i
            participants_row['summonerId'] = participants3[count2]
            count2 = count2+1
            participants_row['gameId'] = last_match2['gameId']
            participants_row['champion'] = row['championId']
            participants_row['win'] = row['stats']['win']
            participants_row['kills'] = row['stats']['kills']
            participants_row['deaths'] = row['stats']['deaths']
            participants_row['assists'] = row['stats']['assists']
            participants_row['totalDamageDealt'] = row['stats']['totalDamageDealtToChampions']
            participants_row['goldEarned'] = row['stats']['goldEarned']
            participants_row['champLevel'] = row['stats']['champLevel']
            participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
            participants_row['role'] = row['timeline']['role']
            participants_row['lane'] = row['timeline']['lane']
            participants_row['spell1Id'] = row['spell1Id']
            participants_row['spell2Id'] = row['spell2Id']
            participants_row['teamId'] = row['teamId']

            participants.append(participants_row)

    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(my_region)[
        'n']['champion']
    # Lets get some champions static information
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    # champ static list data to dict for looking up
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    for row in participants:
        # print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])])
        row['championName'] = champ_dict[str(row['champion'])]

    df = pd.DataFrame(participants)

    hello = df.groupby(by=["gameId", 'teamId'], dropna=False)
    myTeam = pd.DataFrame()
    enemyTeam = pd.DataFrame()
    for key, item in hello:
        data = hello.get_group(key)
        if my_id in data.values:
            if myTeam.empty:
                myTeam = data
            else:
                myTeam = myTeam.append(data)
        else:
            if enemyTeam.empty:
                enemyTeam = data
            else:
                enemyTeam = enemyTeam.append(data)

                # print(hello.get_group(key),  "\n\n")

    my_jungle_games = myTeam.loc[(myTeam['summonerId'] == my_id) & (
        (myTeam['spell1Id'] == 11) | ((myTeam['spell2Id'] == 11)))]
    enemy_jungle_games = enemyTeam.loc[(
        enemyTeam['spell1Id'] == 11) | (enemyTeam['spell2Id'] == 11)]

    # enemy_size = enemy_jungle_games.shape[0]
    # my_size = my_jungle_games.shape[0]
    # arrayIndex = []
    # if enemy_size > my_size:
    #     for row in range(enemy_size, my_size, -1):
    #         print("sup", row)
    #         arrayIndex.append(row-1)
    # enemy_jungle_games = enemy_jungle_games.drop(
    #     enemy_jungle_games.index[arrayIndex])
    # print(my_jungle_games)
    # ax = my_jungle_games.plot(kind="line", x='gameCount',
    #                           y='totalDamageDealt', marker='o', label=summoner_name)
    # enemy_jungle_games.plot(ax=ax, kind='line', x='gameCount',
    #                         y='totalDamageDealt', marker='o', label="Enemy")

    # plt.title("Damage done across 100 games")
    # plt.legend()
    # plt.xlabel("Game Count")
    # plt.ylabel("Damage Done")

    # plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    # plt.xticks(
    #     rotation=45,
    #     horizontalalignment='right',
    #     fontweight='light',
    #     fontsize='x-large'
    # )

    # imgdata = io.BytesIO()

    # plt.savefig(imgdata, format='svg')
    # plt.figure(figsize=(24,7))

    # imgdata.seek(0)  # rewind the data
    # binary_file_data = imgdata.getvalue()
    # base64_encoded_data = base64.b64encode(binary_file_data)
    # base64_message = base64_encoded_data.decode('utf-8')
    # damage_big = largeScaleGraph(
    #     my_jungle_games, enemy_jungle_games, 'gameCount', 'totalDamageDealt', summoner_name)

    damage_data = damageDone(
        my_jungle_games, enemy_jungle_games, summoner_name)
    gold_data = goldEarned(
        my_jungle_games, enemy_jungle_games, summoner_name)

    # dataArray = [base64_message, damage_big, gold_data]
    # dataObject = {
    #     damage: [base64_message, damage_big],
    #     gold:}

    dataArray = [damage_data, gold_data]

    return dataArray


def damageDone(my_jungle_games, enemy_jungle_games, summoner_name):
    enemy_size = enemy_jungle_games.shape[0]
    my_size = my_jungle_games.shape[0]
    arrayIndex = []
    if enemy_size > my_size:
        for row in range(enemy_size, my_size, -1):
            print("sup", row)
            arrayIndex.append(row-1)
    enemy_jungle_games = enemy_jungle_games.drop(
        enemy_jungle_games.index[arrayIndex])
    print(my_jungle_games)
    ax = my_jungle_games.plot(kind="line", x='gameCount',
                              y='totalDamageDealt', marker='o', label=summoner_name)
    enemy_jungle_games.plot(ax=ax, kind='line', x='gameCount',
                            y='totalDamageDealt', marker='o', label="Enemy")
    numberGames = my_jungle_games.shape[0]
    stitle = str(numberGames) + " games"
    plt.title("Damage done across" + stitle)
    plt.legend()
    plt.xlabel("Game Count")
    plt.ylabel("Damage Done")
    imgdata = io.BytesIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    binary_file_data = imgdata.getvalue()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    damage_big = largeScaleGraphTest(
        my_jungle_games, enemy_jungle_games, 'gameCount', 'totalDamageDealt', summoner_name)
    data = [base64_message, damage_big]
    return data


def goldEarned(my_jungle_games, enemy_jungle_games, summoner_name):
    enemy_size = enemy_jungle_games.shape[0]
    my_size = my_jungle_games.shape[0]
    arrayIndex = []
    if enemy_size > my_size:
        for row in range(enemy_size, my_size, -1):
            print("sup", row)
            arrayIndex.append(row-1)
    enemy_jungle_games = enemy_jungle_games.drop(
        enemy_jungle_games.index[arrayIndex])
    ax = my_jungle_games.plot(kind="line", x='gameCount',
                              y='goldEarned', marker='o', label=summoner_name)
    enemy_jungle_games.plot(ax=ax, kind='line', x='gameCount',
                            y='goldEarned', marker='o', label="Enemy")
    gngames = my_jungle_games.shape[0]
    sgtitle = str(gngames) + " games"
    plt.title("Gold Earned across" + sgtitle)
    plt.legend()
    plt.xlabel("Game Count")
    plt.ylabel("Gold Earned")
    imgdata = io.BytesIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    binary_file_data = imgdata.getvalue()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    gold_big = largeScaleGraphTest(
        my_jungle_games, enemy_jungle_games, 'gameCount', 'goldEarned', summoner_name)
    dataArray = [base64_message, gold_big]
    return dataArray


def largeScaleGraph(jungle_games, ejungle_games, x, y, summoner_name):
    ax = jungle_games.plot(kind="line", x=x,
                           y=y, marker='o', label=summoner_name)
    ejungle_games.plot(ax=ax, kind='line', x=x,
                       y=y, marker='o', label="Enemy")

    numberGames = str(jungle_games.shape[0])
    strPlot = numberGames + 'games'
    plt.title(y + "across" + strPlot)
    plt.legend()
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-large'
    )
    plt.xlabel(x)
    plt.ylabel(y)
    imgdta = io.BytesIO()
    plt.rcParams["figure.figsize"] = (24, 7)

    plt.savefig(imgdta, format='svg')
    imgdta.seek(0)  # rewind the data
    binary_file_data = imgdta.getvalue()
    data_Encode = base64.b64encode(binary_file_data)
    largeGraph = data_Encode.decode('utf-8')
    return largeGraph


def largeScaleGraph2(jungle_games, ejungle_games, x, y, summoner_name):
    ax = jungle_games.plot(kind="line", x=x,
                           y=y, marker='o', label=summoner_name)
    ejungle_games.plot(ax=ax, kind='line', x=x,
                       y=y, marker='o', label="Enemy")

    numberGames = str(jungle_games.shape[0])
    strPlot = numberGames + 'games'
    plt.title(y + "across" + strPlot)
    plt.legend()
    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.xticks(
        rotation=45,
        horizontalalignment='right',
        fontweight='light',
        fontsize='x-large'
    )
    plt.xlabel(x)
    plt.ylabel(y)
    imgdta = io.BytesIO()
    plt.rcParams["figure.figsize"] = (24, 7)

    plt.savefig(imgdta, format='svg')
    imgdta.seek(0)  # rewind the data
    binary_file_data = imgdta.getvalue()
    data_Encode = base64.b64encode(binary_file_data)
    largeGraph = data_Encode.decode('utf-8')
    return largeGraph


class dataObject:
    def __init__(self, damage, gold):
        self.damage = damage
        self.gold = gold
