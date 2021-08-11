import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.ticker as mticker
from matplotlib.pyplot import figure


def largeScaleGraphTest(jungle_games, ejungle_games, x, y, summoner_name):
    plt.rcParams["figure.figsize"] = (36, 7)

    print("called")
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
    plt.tick_params(axis='x', which='major',  labelsize=16)
    plt.tick_params(axis='y', which='major',  labelsize=16)
    plt.xlabel(x)
    plt.ylabel(y)
    imgdta = io.BytesIO()

    plt.savefig(imgdta, format='svg')
    imgdta.seek(0)  # rewind the data
    binary_file_data = imgdta.getvalue()
    data_Encode = base64.b64encode(binary_file_data)
    largeGraph = data_Encode.decode('utf-8')
    plt.style.use('default')
    return largeGraph
