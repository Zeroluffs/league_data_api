from riotwatcher import LolWatcher, ApiError
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.ticker as mticker
from matplotlib.pyplot import figure
from api_app.plotting.functions import largeScaleGraphTest


def damage_dealt(summoner_name, nGames, region):

    api_key = 'RGAPI-bed477c4-5dd4-48cd-8711-a6d10f9ce83f'
    watcher = LolWatcher(api_key)
    my_region = 'na1'
    me = watcher.summoner.by_name(region, summoner_name)
    my_id = me['puuid']

   # Return the rank status for me
    my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    my_matches = watcher.match_v5.matchlist_by_puuid(
        'AMERICAS', puuid=my_id, queue='420', type='ranked', count=nGames)

    participants = []
    gameCount = 1
    for n in range(nGames):
        match_detail = watcher.match_v5.by_id(
            region="AMERICAS", match_id=my_matches[n])
        filteredList = list(filter(lambda player: (
            player['individualPosition'] == 'UTILITY' and player['teamPosition'] == 'UTILITY'), match_detail['info']['participants']))
        k = len(filteredList)

        for i in range(k):
            data_dict = filteredList[i]
            data_dict['championName']
            participants_row = {}
            participants_row['gameCount'] = gameCount
            participants_row['championName'] = data_dict["championName"]
            participants_row['puuid'] = data_dict["puuid"]
            participants_row['championId'] = data_dict["championId"]
            participants_row['win'] = data_dict["win"]
            participants_row['kills'] = data_dict["kills"]
            participants_row['deaths'] = data_dict["deaths"]
            participants_row['assists'] = data_dict["assists"]
            participants_row['totalDamageDealtToChampions'] = data_dict["totalDamageDealtToChampions"]
            participants_row["totalDamageTaken"] = data_dict["totalDamageTaken"]
            participants_row['goldEarned'] = data_dict["goldEarned"]
            participants_row['totalMinionsKilled'] = data_dict["totalMinionsKilled"]
            participants_row["wardsPlaced"] = data_dict["wardsPlaced"]
            participants_row["wardsKilled"] = data_dict["wardsKilled"]
            participants_row["visionScore"] = data_dict["visionScore"]
            participants_row["visionWardsBoughtInGame"] = data_dict["visionWardsBoughtInGame"]
            participants_row["totalHealsOnTeammates"] = data_dict["totalHealsOnTeammates"]
            participants_row["totalTimeSpentDead"] = data_dict["totalTimeSpentDead"]
            participants_row["totalDamageShieldedOnTeammates"] = data_dict["totalDamageShieldedOnTeammates"]
            participants.append(participants_row)
        gameCount = gameCount + 1

    df = pd.DataFrame(participants)
    personal_data = df.loc[(df['puuid'] == my_id)]
    enemy_data = df.loc[(df['puuid'] != my_id)]
    damage_data = damageDone(
        personal_data, enemy_data, summoner_name)
    gold_data = goldEarned(
        personal_data, enemy_data, summoner_name)

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
                              y='totalDamageDealtToChampions', marker='o', label=summoner_name)
    enemy_jungle_games.plot(ax=ax, kind='line', x='gameCount',
                            y='totalDamageDealtToChampions', marker='o', label="Enemy")
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
        my_jungle_games, enemy_jungle_games, 'gameCount', 'totalDamageDealtToChampions', summoner_name)
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
