# -*- coding: utf-8 -*-
"""GloVe_enhanced_CNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Bg06xFR5ylBon2tPWUeJj9bjdr2hhJy

# Import Dependencies
"""

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, Conv1D, MaxPooling1D, Dense, Dropout, LSTM
from keras.models import Sequential
from keras.metrics import Precision, Recall
from keras.callbacks import EarlyStopping
from keras import backend

"""# Mount Google Drive To Load Dataset And Save Best Model"""

from google.colab import drive
drive.mount('/content/drive')

"""# Load Balanced Dataset"""

balanced_data = pd.read_csv('/content/drive/MyDrive/NLP/Project/Dataset/HateSpeechDatasetBalanced.csv')

"""# Show Basic Dataset Info"""

balanced_data.info()

# 0 means not hateful
# 1 means hateful
balanced_data['Label'].value_counts()

"""# Split Data Into Training & Validation Sets With An 80/20 Split"""

# Split the dataframe into features (X) and labels (y)
X = balanced_data['Content']
y = balanced_data['Label']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

"""# Tokenize the Data"""

# use only the to 10000 unique words
max_words = 10000

# tokenize the text data
tokenizer = Tokenizer(num_words=max_words, lower=True)
tokenizer.fit_on_texts(X_train)

# print the number of unique tokens in the dataset
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

max_len = 50

# Convert X_train and X_val to list of indicies from the tokenizer
sequences_train = tokenizer.texts_to_sequences(X_train)
sequences_val=tokenizer.texts_to_sequences(X_val)
X_train = pad_sequences(sequences_train,maxlen=max_len)
X_val = pad_sequences(sequences_val,maxlen=max_len)

"""# Load GloVe Embeddings"""

word_vectors = dict()

# load pre-trained GloVe embeddings
f = open('/content/drive/MyDrive/NLP/Project/GloVe Embeddings/glove.twitter.27B.200d.txt', encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_vectors[word] = coefs
f.close()
print('Loaded %s word vectors.' % len(word_vectors))

num_tokens = len(word_index) + 1
embedding_dim = 200
hits = 0
misses = 0

# Prepare embedding matrix with all zoroes
embedding_matrix = np.zeros((num_tokens, embedding_dim))
for word, i in word_index.items():
    embedding_vector = word_vectors.get(word)
    if embedding_vector is not None:
        # Words not found in embedding index will be all-zeros.
        # This includes the representation for "padding" and "OOV"
        embedding_matrix[i] = embedding_vector
        hits += 1
    else:
        misses += 1
print("Converted %d words (%d misses)" % (hits, misses))

"""# Create Embeddings Layer"""

# create the embeddings layer
embedding_layer = Embedding(
    num_tokens,
    embedding_dim,
    trainable=False,
    name="GloVe"
)
embedding_layer.build((1,))
embedding_layer.set_weights([embedding_matrix])

"""# Build The CNN"""

# custom metric callback to pass to model.compile
def f1_metric(y_true, y_pred):
    y_true = tf.cast(y_true, "int32")
    y_pred = tf.cast(tf.round(y_pred), "int32")  # round predictions to closest integer (0 or 1)
    tp = tf.reduce_sum(tf.cast(tf.math.logical_and(tf.equal(y_true, 1), tf.equal(y_pred, 1)), "float32"), axis=0)
    fp = tf.reduce_sum(tf.cast(tf.math.logical_and(tf.equal(y_true, 0), tf.equal(y_pred, 1)), "float32"), axis=0)
    fn = tf.reduce_sum(tf.cast(tf.math.logical_and(tf.equal(y_true, 1), tf.equal(y_pred, 0)), "float32"), axis=0)

    precision = tp / (tp + fp + backend.epsilon())
    recall = tp / (tp + fn + backend.epsilon())

    f1 = 2 * precision * recall / (precision + recall + backend.epsilon())
    f1_score = tf.reduce_mean(f1)

    return f1_score

# create the GloVe enhanced CNN
model = Sequential()
model.add(embedding_layer)

model.add(Conv1D(64, 5, activation="relu"))
model.add(MaxPooling1D())
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dense(32, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['accuracy', Precision(), Recall(), f1_metric])
model.summary()

# get training data
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)

# get validation data
X_val = np.asarray(X_val)
y_val = np.asarray(y_val)

history = model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_val, y_val), callbacks=EarlyStopping(monitor='val_loss', patience=2))

import matplotlib.pyplot as plt

# get training and validation loss from training history
train_loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(train_loss) + 1)

# plot training and validation loss
plt.plot(epochs, train_loss, color='blue', label='Train Loss')
plt.plot(epochs, val_loss, color='orange', label='Validation Loss')

# set plot and axis titles
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

# set x ticks and add a legend
plt.xticks(range(1, len(train_loss) + 1))
plt.legend()

# show the plot
plt.show()

# plot the model architecture
tf.keras.utils.plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=False)