# import module
from faulthandler import disable
import streamlit as st
import time
import datetime
import prediction
import json
import pandas as pd
import threading 
from accuracy import accuracy


st.set_page_config(
    page_title="LSTM Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",

    )


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
            content:'Developed by Sujatha'; 
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
                 }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
city=pd.read_csv('cities_predict.csv')
f = open("train_time.json")
fd = json.load(f)
date=fd["last_train_date"]
st.write("Model Last Train date: ",date)



def model_train():
    while True:
        import train
        train.train()
        time.sleep(10)  

def main():
    try :
        pollutant = st.selectbox("Type of Pollutant: ",
                        ['no2', 'so2', 'pm2_5', 'pm10', 'o3', 'nh3', 'no'])
    
        cities = st.multiselect(
            "Choose cities", city.cityName, city.cityName[0]
        )
        days = st.slider("No of days need to be predict ", 7, 40)
        sp=time.time()
        with st.spinner('Please Wait...'):
            df=prediction.prediction(cities,days,pollutant)
            acq=accuracy(cities)
        ep=time.time()
        timeElapsed=ep-sp
        col1,col2=st.columns([3,1])
        with col1:
            st.write("Predicition time elapsed in seconds : ",timeElapsed)
        with col2:
            st.button("i",disabled=True,help=acq)
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


if __name__ == "__main__":
    main()
    t2 = threading.Thread(target=model_train)
    t2.start()
	