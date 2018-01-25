import pandas as pd
import numpy as np
import re
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

"""
Trains machine learning model on dataset of tweets labeled with net sentiment (1 or 0)
Dataset from: http://thinknook.com/twitter-sentiment-analysis-training-corpus-dataset-2012-09-22/
"""

# Read in training data:
df = pd.read_csv('data.csv', error_bad_lines=False)
df = df.drop(['ItemID', 'SentimentSource'], axis=1)

# Separate data and labels:
X = df.drop(['Sentiment'], axis=1)
y = df.drop(['SentimentText'], axis=1)

# Clean data:
for i, row in X.iterrows():
    val = row['SentimentText']
    val = re.sub('\.', ' . ', val)
    X.set_value(i,'SentimentText',val)

# Tokenize input data:
tokenizer = Tokenizer(filters='"#%&+,-<=>@[\]^_`{|}~\t\n')
tokenizer.fit_on_texts(X['SentimentText'])
X = tokenizer.texts_to_sequences(X['SentimentText'])
X = pad_sequences(X, maxlen=140, padding='post')

# Save tokenizer for later:
with open('./tokenizer.pickle', 'wb') as f:
    pickle.dump(tokenizer, f)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=52)

# Train model on data and save it to file:
clf = RandomForestClassifier(max_depth=10, random_state=52)
clf.fit(X_train, y_train)

with open('./classifier.pickle', 'wb') as f:
    pickle.dump(clf, f)

# Display accuracy score:
num_incorrect_preds = 0
for i, row in df2.iterrows():
    if row['actual'] != row['preds']:
        num_incorrect_preds += 1
print("Accuracy: ", 1 - num_incorrect_preds/df2.size)
