import json
from datetime import datetime
import dateutil.parser
import matplotlib.pyplot as plt
import pandas as pd
from darts import TimeSeries
import numpy as np

# insert json file path here

def get_individual_statistics(file): #filepath here
    file_path = file 

    with open(file_path) as f:
        data = json.loads(f.read())
        msgs = data['messages']

    df = pd.DataFrame(msgs)

    df_new = df.filter(items=["from", "date"])
    df_new = df_new.sort_values(by="date")


    def get_total_messages_sent(df):
        df_new = df
        df_new = df_new.groupby(by="from").count()
        print(df_new)
        return df_new


    return get_total_messages_sent(df_new)



get_individual_statistics("yijie3.json")