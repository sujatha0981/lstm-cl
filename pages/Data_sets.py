import streamlit as st
import os
import pandas as pd
import json 

st.set_page_config(
   page_title="Dataset",
   page_icon="📂",
   layout="wide",
   initial_sidebar_state="expanded",
)

city=pd.read_csv('cities_predict.csv')
f = open("train_time.json")
fd = json.load(f)
date=fd["last_train_date"]
st.write("Dataset scraped on : ",date)

st.write("Download Datase :")

for x in os.listdir('./data'):
    if x.endswith(".csv"):
        x1="./data/"+x
        with open(x1, "rb") as file:
                btn = st.download_button(
                        label=x,
                        data=file,
                        file_name=x,
                    )
for x in os.listdir():
    if x.endswith(".json"):
        # Prints only text file present in My Folder
        if x!="train_time.json":
            with open(x, "rb") as file:
                btn = st.download_button(
                        label=x,
                        data=file,
                        file_name=x,
                    )
