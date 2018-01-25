import pickle
import pandas as pd
import numpy as np
import re
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

"""
Apply trained model to predict the sentiment of tweets saved from stream_tweets
"""

# Load tokenizer and trained model:
with open('./tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)
with open('./classifier.pickle', 'rb') as f:
    clf = pickle.load(f)

# Load in streamed tweets
df = pd.read_csv('tweets.csv', sep=';;', error_bad_lines=False)
pd.set_option('max_colwidth',180)
df = df.drop(['Unnamed: 1'], axis=1)

# Clean tweets to match format of training data:
for i, row in df.iterrows():
    val = row['tweets']
    val = re.sub('\.', ' . ', val)
    df.set_value(i,'tweets',val)

# Tokenize tweets:
X = tokenizer.texts_to_sequences(df['tweets'])
X = pad_sequences(X, maxlen=140, padding='post')

# Apply model:
preds = clf.predict(X)
df['preds'] = preds

# Convey overall sentiment of tweets:
num_positive = 0
for pred in preds:
    if pred == 1:
        num_positive += 1
print("Overall sentiment: ", str((num_positive / len(preds)) * 100)[:5], "% positive")