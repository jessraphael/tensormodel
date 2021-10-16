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




###########################################################

#Calculate Reviews
r = requests.get('https://www.yelp.com/biz/social-brew-cafe-pyrmont')
soup = BeautifulSoup(r.text, 'html.parser')
regex = re.compile('.*comment.*')
results = soup.find_all('p', {'class':regex})
reviews = [result.text for result in results]

