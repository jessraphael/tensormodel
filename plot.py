
import json
from datetime import datetime
import dateutil.parser
import matplotlib.pyplot as plt

f = open('jiawei.json')

data = json.load(f)

timing = []
timeDiff = []
x_value = []

for i in data["messages"]:
    initial = dateutil.parser.isoparse(i["date"]).timestamp()
    timing.append(initial)

for x in range(1,len(timing)):
    initial = timing[x-1]
    final = timing[x]
    timeDiff.append(final-initial)

for x in range(0,len(timeDiff)):
    x_value.append(x)

plt.plot(x_value,timeDiff)

plt.show()




