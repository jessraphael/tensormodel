from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import re


#Model Instantiation 
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')


#Encode and calculate sentiment
tokens = tokenizer.encode('It was bad but couldve been better. Lmao', return_tensors='pt')

result = model(tokens)

result.logits

print(int(torch.argmax(result.logits))+1)

#Calculate Reviews
r = requests.get('https://www.yelp.com/biz/social-brew-cafe-pyrmont')
soup = BeautifulSoup(r.text, 'html.parser')
regex = re.compile('.*comment.*')
results = soup.find_all('p', {'class':regex})
reviews = [result.text for result in results]

#Load Reviews into DataFrame and Score

df = pd.DataFrame(np.array(reviews), columns=['review'])
df['review'].iloc[0]


def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)

sentiment_score(df['review'].iloc[1])

df['sentiment'] = df['review'].apply(lambda x: sentiment_score(x[:512]))
df['review'].iloc[3]
