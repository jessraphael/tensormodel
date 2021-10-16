
import json
from datetime import datetime
from os import wait
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd
from darts import TimeSeries
import numpy as np


def runfile(filepath):

    file_path = filepath

    with open(file_path) as f:
        data = json.loads(f.read())
        msgs = data['messages']

    df = pd.DataFrame(msgs)

    df_new = df.filter(items= ["from", "date"])
    df_new = df_new.sort_values(by="date")


    def getTimeDiff(df):
        output = []


        for x in range(0, len(df)):
         if x != 0 and df.iloc[x][0] != df.iloc[x-1][0]:
                username = df.iloc[x][0]
                timeDiff = (dateutil.parser.isoparse(df.iloc[x][1]).timestamp()) - (dateutil.parser.isoparse(df.iloc[x-1][1]).timestamp()) 
                output.append(timeDiff)
        return output

    y= getTimeDiff(df_new)
    x= list(range(1,len(y)+1))

    average_waiting_time =  sum(y)/len(x)

    plt.plot(x,y)
    plt.show()

runfile("result.json")