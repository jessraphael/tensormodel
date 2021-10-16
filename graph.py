import json
from datetime import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd
from darts import TimeSeries
import numpy as np

## insert json file path here
def get_time_diff(file_path):

    with open(file_path) as f:
        data = json.loads(f.read())
        msgs = data['messages']

    df = pd.DataFrame(msgs)

    df_new = df.filter(items= ["from", "date"])
    df_new = df_new.sort_values(by="date")


    print(df_new)

    def getTimeDiff(df):
        output = []


        for x in range(0, len(df)):
            if x != 0 and df.iloc[x][0] != df.iloc[x-1][0]:
                username = df.iloc[x][0]
                timeDiff = (dateutil.parser.isoparse(df.iloc[x][1]).timestamp()) - (dateutil.parser.isoparse(df.iloc[x-1][1]).timestamp())
                output.append(timeDiff)
        return output

    y= getTimeDiff(df_new)

    return y

def get_number_of_instances(y):
    return list(range(1,len(y)+1))

def get_average_waiting_time_in_seconds(x,y):    
    return sum(y)/len(x)

def plot_graph(x,y):
    plt.plot(x,y)
    plt.title("Response rate vs number of texting instances")
    return plt.show()