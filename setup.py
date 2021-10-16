from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
import re

class Model_Manager():
    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    def __init__(self):
