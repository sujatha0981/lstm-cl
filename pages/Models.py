import streamlit as st
import os
import pandas as pd
import json 

st.set_page_config(
   page_title="Models",
   page_icon="📂",
   layout="wide",
   initial_sidebar_state="expanded",
)

city=pd.read_csv('cities_predict.csv')
f = open("train_time.json")
fd = json.load(f)
date=fd["last_train_date"]
st.write("Model Last Train date : ",date)

st.write("Download Model :")

for x in os.listdir('./saved_model'):
    if x.endswith(".h5"):
        x1="./saved_model/"+x
        with open(x1, "rb") as file:
                btn = st.download_button(
                        label=x,
                        data=file,
                        file_name=x,
                    )