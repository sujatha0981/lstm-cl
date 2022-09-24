import streamlit as st
import numpy as np
import pandas as pd
import time
import prediction
df=prediction.prediction(['Chennai','Bengaluru'],40)
chart = st.line_chart(df.iloc[0:6])

for i in range(7, len(df)):
    chart.add_rows(df.iloc[i:i+1])
    time.sleep(0.05)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
