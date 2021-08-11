from riotwatcher import LolWatcher, ApiError
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.ticker as mticker
from matplotlib.pyplot import figure
from api_app.plotting.functions import largeScaleGraphTest
from matplotlib.ticker import MaxNLocator


def damage_dealt(summoner_name, nGames, region, role, data):

    api_key = 'RGAPI-512438ee-6be0-4c87-852e-6d88151224d4'
    watcher = LolWatcher(api_key)
    my_region = 'na1'
    me = watcher.summoner.by_name(region, summoner_name)
    my_id = me['puuid']
    print(my_id)
   # Return the rank status for me
    my_matches = watcher.match_v5.matchlist_by_puuid(
        'AMERICAS', puuid=my_id, queue='420', type='ranked', count=nGames)

    participants = []
    gameCount = 0

    if role == "jg":
        individualPosition = "JUNGLE"
        teamPosition = "JUNGLE"
    if role == "top":
        individualPosition = "TOP"
        teamPosition = "TOP"
    if role == "mid":
        individualPosition = "MIDDLE"
        teamPosition = "MIDDLE"
    if role == "adc":
        individualPosition = "BOTTOM"
        teamPosition = "BOTTOM"
    if role == "supp":
        individualPosition = "UTILITY"
        teamPosition = "UTILITY"

    for n in range(nGames):
        match_detail = watcher.match_v5.by_id(
            region="AMERICAS", match_id=my_matches[n])
        filteredList = list(filter(lambda player: (
            player['individualPosition'] == individualPosition and player['teamPosition'] == teamPosition), match_detail['info']['participants']))
        k = len(filteredList)
        for i in range(k):
            if k == 2:
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
                participants_row["damageDealtToObjectives"] = data_dict["damageDealtToObjectives"]
                participants_row["damageDealtToTurrets"] = data_dict["damageDealtToTurrets"]
                participants_row["damageSelfMitigated"] = data_dict["damageSelfMitigated"]
                participants_row["dragonKills"] = data_dict["dragonKills"]
                participants_row["objectivesStolen"] = data_dict["objectivesStolen"]
                participants_row["turretKills"] = data_dict["turretKills"]
                participants_row["turretsLost"] = data_dict["turretsLost"]
                participants_row["turretTakedowns"] = data_dict["turretTakedowns"]



                participants.append(participants_row)
        gameCount = gameCount + 1

    df = pd.DataFrame(participants)
    personal_data = df.loc[(df['puuid'] == my_id)]
    print(personal_data['totalDamageDealtToChampions'])

    enemy_data = df.loc[(df['puuid'] != my_id)]
    print(len(enemy_data['totalDamageDealtToChampions']))
    dataArray = roleData(personal_data, enemy_data, summoner_name, data)
    return dataArray


def roleData(personal_data, enemy_data, summoner_name, data):
    yLabelString = data
    yLabels = data
    n = len(yLabels)
    arrayWithData = []
    for i in range(n):
        array = normalSizedgraph(
            personal_data, enemy_data, summoner_name, yLabels[i], yLabelString[i])
        arrayWithData.append(array)
    return arrayWithData


def normalSizedgraph(personal_games, enemy_games, summoner_name, yLabel, yLabelString):
    ax = personal_games.plot(kind="line", x='gameCount',
                             y=yLabel, marker='o', label=summoner_name)
    enemy_games.plot(ax=ax, kind='line', x='gameCount',
                     y=yLabel, marker='o', label="Enemy")
    gngames = personal_games.shape[0]
    sgtitle = str(gngames) + " games"
    plt.title(yLabelString + " across" + " " + sgtitle)
    plt.legend()
    plt.xlabel("Game Count")
    plt.ylabel(yLabelString)
    plt.xlim(1, gngames)
    imgdata = io.BytesIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    binary_file_data = imgdata.getvalue()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_message = base64_encoded_data.decode('utf-8')
    gold_big = largeScaleGraphTest(
        personal_games, enemy_games, 'gameCount', yLabel, summoner_name)
    dataArray = [base64_message, gold_big]
    return dataArray
