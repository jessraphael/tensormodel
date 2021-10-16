import json
from datetime import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd
from darts import TimeSeries
import numpy as np


file_path = "yijie3.json"
with open(file_path) as f:
        data = json.loads(f.read())
        msgs = data['messages']

df = pd.DataFrame(msgs)

df_new = df.filter(items= ["from", "date"])
df_new = df_new.sort_values(by="date")


print(df_new)
# def getDays(df):
#     output = []
#     for x in range(0, len(df)):
#         date_time = datetime.strptime(df.iloc[x][1], '%Y-%m-%dT%H:%M:%S').date()
#         if date_time not in output:
#             output.append(df.iloc[x][1])
#     unique_dates = list(set(output))

#     return unique_dates



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

print(x)
print(y)

plt.plot(x,y)
plt.title("Response rate vs number of texting instances")
plt.show()