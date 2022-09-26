# import module
import streamlit as st
import time
import datetime
import prediction
import json
import pandas as pd


st.set_page_config(
   page_title="LSTM Model",
   page_icon="📈",
   layout="wide",
   initial_sidebar_state="expanded",
)
city=pd.read_csv('cities.csv')
f = open("train_time.json")
fd = json.load(f)
date=fd["last_train_date"]
st.write("Model Last Train date: ",date)
with st.spinner('Model training Please Wait...'):
    import train
# Title
train.train()
try :
    pollutant = st.selectbox("Type of Pollutant: ",
                     ['no2', 'so2', 'pm2_5', 'pm10', 'o3', 'nh3', 'no'])
 
    cities = st.multiselect(
        "Choose cities", city.cityName, city.cityName[0]
    )
    days = st.slider("No of days need to be predict ", 7, 40)
    with st.spinner('Please Wait...'):
        df=prediction.prediction(cities,days,pollutant)
    
    chart = st.line_chart(df.iloc[0:6])

    for i in range(7, len(df)):
        chart.add_rows(df.iloc[i:i+1])
        time.sleep(0.05)
    
    st.write(df)
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download Prediction",
        data=csv,
        file_name='lstm_prediction.csv',
    )
except :
    st.title("error !!!")