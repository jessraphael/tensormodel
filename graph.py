
import json
from datetime import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd


f = open('jiawei.json')

data = json.loads(f)


dataframe = pd.DataFrame.from_dict(data, orient="index")

print(dataframe)