from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
import torch
import re
import json
import os
from flask import Flask, render_template, make_response
from flask import request

# Setting up model
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

port = int(os.getenv('PORT'))
host = "whalefoodai.herokuapp.com"

def get_unique_users(msgs):
    users = []
    for msg in msgs:
        temp_user = msg['from']
        if temp_user not in users:
            users.append(temp_user)
        if len(users) > 1:
            break
    return users


def categorize_messages_by_sender(msgs):
    senders = get_unique_users(msgs)
    msg1 = []
    msg2 = []

    for msg in msgs:
        if msg['from'] == senders[0]:
            msg1.append(msg['text'])
        else:
            msg2.append(msg['text'])

    return {senders[0]: msg1, senders[1]: msg2}


def getting_score(message):
    tokens = tokenizer.encode(message, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def getting_avg_score(all_msgs):
    total_score = 0

    for msg in all_msgs:
        total_score += getting_score(msg)
    return total_score / len(all_msgs)


def getting_all_avg_scores(all_msgs):
    msgs = categorize_messages_by_sender(all_msgs)
    users = list(msgs.keys())
    output = {}
    for user in users:
        score = getting_avg_score(msgs[user])
        output[user] = score
    return output


from datetime import datetime


def getting_unique_dates(msgs):
    all_dates = []
    for msg in msgs:
        date_time = datetime.strptime(msg['date'], '%Y-%m-%dT%H:%M:%S')
        d = date_time.date()
        all_dates.append(d)
    unique_dates = list(set(all_dates))
    return unique_dates


def get_all_msgs_on_date(msgs, selected_date):
    output = []
    for msg in msgs:
        msg_date = datetime.strptime(msg['date'], '%Y-%m-%dT%H:%M:%S').date()
        if msg_date == selected_date:
            output.append(msg)
    return output


def sentiment_analysis(data):
    msgs = data['messages']

    unique_dates = getting_unique_dates(msgs)
    output = {}

    for unique_date in unique_dates:
        temp_msgs = get_all_msgs_on_date(msgs, unique_date)
        scores = getting_all_avg_scores(temp_msgs)
        temp = {}
        for user in scores:
            temp[user] = scores[user]
        output[unique_date.strftime('%Y-%m-%dT%H:%M:%S')] = temp

    return output


app = Flask(__name__)


@app.route('/get_sentiment_score', methods=['POST'])
def get_sentiment_score():
    data = request.get_json()
    data = json.loads(data)
    output = sentiment_analysis(data)

    return make_response(output, 200)


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(threaded=True, debug=False, port=port)