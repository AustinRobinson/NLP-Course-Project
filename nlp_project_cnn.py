# -*- coding: utf-8 -*-
"""NLP Project CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CEinhSzcZcVmuJncFjMs0W30iYTvbR7J
"""

import pandas as pd

# Load data from CSV
df = pd.read_csv('HateSpeechDatasetBalanced.csv')

print(df['Label'].isnull().sum())

df.dropna(subset=['Label'], inplace=True)

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from keras.regularizers import l2
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler

# Load data from CSV
df = pd.read_csv('HateSpeechDatasetBalanced.csv')

# Assuming your CSV has columns named 'text' and 'label'
texts = df['Content'].tolist()
labels = df['Label'].tolist()

# Tokenization
max_words = 10000  # Adjust as needed
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Padding
maxlen = 100  # Adjust as needed
X = pad_sequences(sequences, maxlen=maxlen)
y = np.array(labels)

# Define the learning rate schedule
def lr_schedule(epoch):
    """
    Learning rate schedule function.
    """
    initial_lr = 0.001  # Initial learning rate
    drop = 0.5  # Learning rate drop factor
    epochs_drop = 3  # Number of epochs after which learning rate should drop
    lr = initial_lr * (drop ** (epoch // epochs_drop))
    return lr

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CNN model
model = Sequential()
model.add(Embedding(max_words, 128, input_length=maxlen))
model.add(Conv1D(64, 3, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid', kernel_regularizer=l2(0.01)))

optimizer = Adam(learning_rate=0.001)  # Initial learning rate
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Define learning rate scheduler callback
lr_scheduler = LearningRateScheduler(lr_schedule)

# Lists to store metrics for each epoch
accuracy_list = []
precision_list = []
recall_list = []
f1_list = []

# Model training
for epoch in range(3):  # 3 epochs
    print(f"Epoch {epoch + 1}/5")
    history = model.fit(X_train, y_train, epochs=1, batch_size=32, validation_split=0.2, verbose=2, callbacks=[lr_scheduler])

    # Evaluation on training set
    y_train_pred = (model.predict(X_train) > 0.5).astype(int)
    accuracy_train = accuracy_score(y_train, y_train_pred)
    precision_train = precision_score(y_train, y_train_pred)
    recall_train = recall_score(y_train, y_train_pred)
    f1_train = f1_score(y_train, y_train_pred)

    # Evaluation on validation set
    y_val_pred = (model.predict(X_test) > 0.5).astype(int)
    accuracy_val = accuracy_score(y_test, y_val_pred)
    precision_val = precision_score(y_test, y_val_pred)
    recall_val = recall_score(y_test, y_val_pred)
    f1_val = f1_score(y_test, y_val_pred)

    # Print metrics for each epoch
    print("Training set:")
    print("Accuracy:", accuracy_train)
    print("Precision:", precision_train)
    print("Recall:", recall_train)
    print("F1 Score:", f1_train)

    print("Validation set:")
    print("Accuracy:", accuracy_val)
    print("Precision:", precision_val)
    print("Recall:", recall_val)
    print("F1 Score:", f1_val)
    print()

    # Append metrics to lists
    accuracy_list.append(accuracy_val)
    precision_list.append(precision_val)
    recall_list.append(recall_val)
    f1_list.append(f1_val)

# Plot loss curves for training and validation
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

# Print metrics for each epoch in a table
metrics_df = pd.DataFrame(history.history)
metrics_df.index += 1  # Start indexing epochs from 1
print("\nMetrics for each epoch:")
print(metrics_df)

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from keras.regularizers import l2
from keras.optimizers import Adam
from keras.callbacks import LearningRateScheduler

# Load data from CSV
df = pd.read_csv('HateSpeechDatasetBalanced.csv')

# Assuming your CSV has columns named 'text' and 'label'
texts = df['Content'].tolist()
labels = df['Label'].tolist()

# Tokenization
max_words = 10000  # Adjust as needed
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Padding
maxlen = 100  # Adjust as needed
X = pad_sequences(sequences, maxlen=maxlen)
y = np.array(labels)

# Define the learning rate schedule
def lr_schedule(epoch):
    """
    Learning rate schedule function.
    """
    initial_lr = 0.001  # Initial learning rate
    drop = 0.5  # Learning rate drop factor
    epochs_drop = 3  # Number of epochs after which learning rate should drop
    lr = initial_lr * (drop ** (epoch // epochs_drop))
    return lr

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CNN model
model = Sequential()
model.add(Embedding(max_words, 128, input_length=maxlen))
model.add(Conv1D(64, 3, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid', kernel_regularizer=l2(0.01)))

optimizer = Adam(learning_rate=0.001)  # Initial learning rate
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Define learning rate scheduler callback
lr_scheduler = LearningRateScheduler(lr_schedule)

# Lists to store metrics for each epoch
accuracy_list = []
precision_list = []
recall_list = []
f1_list = []
loss_list = []
val_loss_list = []

# Model training
for epoch in range(3):  # 3 epochs
    print(f"Epoch {epoch + 1}/3")
    history = model.fit(X_train, y_train, epochs=1, batch_size=32, validation_split=0.2, verbose=2, callbacks=[lr_scheduler])

    # Evaluation on training set
    y_train_pred = (model.predict(X_train) > 0.5).astype(int)
    accuracy_train = accuracy_score(y_train, y_train_pred)
    precision_train = precision_score(y_train, y_train_pred)
    recall_train = recall_score(y_train, y_train_pred)
    f1_train = f1_score(y_train, y_train_pred)

    # Evaluation on validation set
    y_val_pred = (model.predict(X_test) > 0.5).astype(int)
    accuracy_val = accuracy_score(y_test, y_val_pred)
    precision_val = precision_score(y_test, y_val_pred)
    recall_val = recall_score(y_test, y_val_pred)
    f1_val = f1_score(y_test, y_val_pred)

    # Print metrics for each epoch
    print("Training set:")
    print("Accuracy:", accuracy_train)
    print("Precision:", precision_train)
    print("Recall:", recall_train)
    print("F1 Score:", f1_train)

    print("Validation set:")
    print("Accuracy:", accuracy_val)
    print("Precision:", precision_val)
    print("Recall:", recall_val)
    print("F1 Score:", f1_val)
    print()

    # Append metrics to lists
    accuracy_list.append(accuracy_val)
    precision_list.append(precision_val)
    recall_list.append(recall_val)
    f1_list.append(f1_val)
    loss_list.append(history.history['loss'][0])
    val_loss_list.append(history.history['val_loss'][0])

# Plot loss curves for training and validation
plt.plot(loss_list, label='Training Loss')
plt.plot(val_loss_list, label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

# Print metrics for each epoch in a table
metrics_df = pd.DataFrame(history.history)
metrics_df.index += 1  # Start indexing epochs from 1
print("\nMetrics for each epoch:")
print(loss_list, val_loss_list)