from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from datetime import datetime

# Setting up model
class SentimentAnalyzer():

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    def get_unique_users(self, msgs):
        users = []
        for msg in msgs:
            temp_user = msg['from']
            if temp_user not in users:
                users.append(temp_user)
            if len(users) > 1:
                break
        return users


    def categorize_messages_by_sender(self, msgs):
        senders = self.get_unique_users(msgs)
        msg1 = []
        msg2 = []

        for msg in msgs:
            if msg['from'] == senders[0]:
                msg1.append(msg['text'])
            else:
                msg2.append(msg['text'])

        return {senders[0]: msg1, senders[1]: msg2}


    def getting_score(self, message):
        tokens = self.tokenizer.encode(message, return_tensors='pt')
        result = self.model(tokens)
        return int(torch.argmax(result.logits)) + 1


    def getting_avg_score(self, all_msgs):
        total_score = 0

        for msg in all_msgs:
            total_score += self.getting_score(msg)
        return total_score / len(all_msgs)


    def getting_all_avg_scores(self, all_msgs):
        msgs = self.categorize_messages_by_sender(all_msgs)
        users = list(msgs.keys())
        output = {}
        for user in users:
            score = self.getting_avg_score(msgs[user])
            output[user] = score
        return output


    def getting_unique_dates(self, msgs):
        all_dates = []
        for msg in msgs:
            date_time = datetime.strptime(msg['date'], '%Y-%m-%dT%H:%M:%S')
            d = date_time.date()
            all_dates.append(d)
        unique_dates = list(set(all_dates))
        return unique_dates


    def get_all_msgs_on_date(self, msgs, selected_date):
        output = []
        for msg in msgs:
            msg_date = datetime.strptime(msg['date'], '%Y-%m-%dT%H:%M:%S').date()
            if msg_date == selected_date:
                output.append(msg)
        return output


    def sentiment_analysis(self, data):
        msgs = data['messages']

        unique_dates = self.getting_unique_dates(msgs)
        output = []
        temp = {'date': "", 'values': ()}

        for unique_date in unique_dates:
            temp['date'] = unique_date.strftime('%Y-%m-%d')
            temp_msgs = self.get_all_msgs_on_date(msgs, unique_date)
            scores = self.getting_all_avg_scores(temp_msgs)
            temp_score_list = []
            for user in scores:
                temp_score_list.append({user: scores[user]})
            temp['values'] = set(temp_score_list)
            output.append(temp)

        return output


sa = SentimentAnalyzer()


def getSA():
    return sa