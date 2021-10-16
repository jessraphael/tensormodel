
import json
from datetime import datetime
from os import SCHED_OTHER
import dateutil.parser
import matplotlib.pyplot as plt


#To get all the dates in the messages sent 
def getting_unique_dates(msgs):
    all_dates = []
    for msg in msgs:
        date_time = datetime.strptime(msg['date'], '%Y-%m-%dT%H:%M:%S')
        d = date_time.date()
        all_dates.append(d)
    unique_dates = list(set(all_dates))
    return unique_dates


#To get all the messages for that specific day itself 
def get_all_msgs_on_date(msgs, selected_date):
    output = []
    for msg in msgs:
        msg_date = datetime.strptime(msg['date'], '%Y-%m-%dT%H:%M:%S').date()
        if msg_date == selected_date:
            output.append(msg)
    return output

def get_time_instance(day_messages):
    timings = []
    timeDiff = []
    output = []

    for i in day_messages:
        
        time_instance = dateutil.parser.isoparse(i["date"]).timestamp()
        username = i["from"]
        timings.append([username, time_instance])

    return timings

def sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li
  


def get_time_difference_between_user(msgs):
    msgs = sort(msgs)
    print(msgs)
    output = []


    for x in range(0,len(msgs)):
        
        if x != 0 and msgs[x][0] != msgs[x-1][0]:
            timeDiff =  msgs[x][1] - msgs[x-1][1] 
            output.append(timeDiff)
    return output


file_path = "jiawei.json"

def run(file_path):
    with open(file_path) as f:
        data = json.loads(f.read())
        msgs = data['messages']

    unique_dates = getting_unique_dates(msgs)[::-1]
        

    print("HAHAHAHAH")
    print(unique_dates)
    output = []

    for x in range(0,len(unique_dates)):
        message = get_all_msgs_on_date(msgs, unique_dates[x])
        msg = get_time_instance(message)
        y = get_time_difference_between_user(msg)
        averageTime = sum(y)/len(y)
        output.append(int(averageTime))
    
    print("HELLO")
    print(x)
    print("WORLD")
    print(output)

    plt.plot(list(range(1,len(output)+1)),output)
    return plt.show()



print(run(file_path))