import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout
import tensorflow as tf
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from datetime import datetime
from rn import fn
import pickle

def model_train(cityNameI):
    
    df = pd.read_csv('data/data_'+cityNameI+'.csv')
    train_dates = pd.to_datetime(df['Date'])
    cols = list(df)[1:8]
    df_for_training = df[cols].astype(float)
    scaler = StandardScaler()
    scaler = scaler.fit(df_for_training)
    df_for_training_scaled = scaler.transform(df_for_training)
    trainX = []
    trainY = []
    n_future = 1  
    n_past = 14  
    for i in range(n_past, len(df_for_training_scaled) - n_future +1):
        trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
        trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])
    trainX, trainY = np.array(trainX), np.array(trainY)
    model1 = Sequential()
    model1.add(LSTM(64, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model1.add(LSTM(32, activation='relu', return_sequences=False))
    model1.add(Dropout(0.2))
    model1.add(Dense(trainY.shape[1]))
    model1.compile(optimizer='adam', loss='mse')
    model1.fit(trainX, trainY, epochs=100, batch_size=7, validation_split=.1, verbose=1)
    os.popen("mkdir saved_model")
    model1.save('saved_model/lstm_model_'+cityNameI+'.h5')
    accuracy = [fn(model1)]
    with open("./saved_model/lstm_model_"+cityNameI+".pkl","wb") as file:
        pickle.dump(accuracy, file)

def model_prediction(cityNameI,no_of_days,pollutantValue):   
    df = pd.read_csv('data/data_'+cityNameI+'.csv')
    train_dates = pd.to_datetime(df['Date'])
    cols = list(df)[1:8]
    df_for_training = df[cols].astype(float)
    scaler = StandardScaler()
    scaler = scaler.fit(df_for_training)
    df_for_training_scaled = scaler.transform(df_for_training)
    trainX = []
    trainY = []
    n_future = 1  
    n_past = 14  
    for i in range(n_past, len(df_for_training_scaled) - n_future +1):
        trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
        trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 0])
    trainX, trainY = np.array(trainX), np.array(trainY)
    model = tf.keras.models.load_model('saved_model/lstm_model_'+cityNameI+'.h5')
    n_past = 16
    n_days_for_prediction=no_of_days 
    predict_period_dates = pd.date_range(list(train_dates)[-n_past], periods=n_days_for_prediction).tolist()
    prediction = model.predict(trainX[-n_days_for_prediction:]) 
    prediction_copies = np.repeat(prediction, df_for_training.shape[1], axis=-1)
    y_pred_future = scaler.inverse_transform(prediction_copies)[:,pollutantValue]
    return y_pred_future

