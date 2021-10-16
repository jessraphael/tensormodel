#Load Reviews into DataFrame and Score

df = pd.DataFrame(np.array(reviews), columns=['review'])
df['review'].iloc[0]


def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)

sentiment_score(df['review'].iloc[1])

df['sentiment'] = df['review'].apply(lambda x: sentiment_score(x[:512]))
df['review'].iloc[3]