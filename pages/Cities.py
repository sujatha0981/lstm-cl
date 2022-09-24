import streamlit as st
import pandas as  pd
import train
from clear import clear
df=pd.read_csv("./cities.csv")


try:
    col1,col2,col3,col4 = st.columns(4)
    col1.write("cityName")
    for i in range(len(df)):
        col1.write(df.loc[i]['cityName'])
    col2.write("latitude")
    for i in range(len(df)):
        col2.write(df.loc[i]['lat'])
    col3.write("longitude")
    for i in range(len(df)):
        col3.write(df.loc[i]['long'])
    col4.write("")
    for i in range(len(df)):
        if col4.button('Delete',key=i):
            clear(df.loc[i]['cityName'])
            df=df.drop(i)     
            df.to_csv("./cities.csv", index=False)
    cityName = st.text_input('City Name')
    lat = st.text_input('latitude')
    long = st.text_input('Longitude')

    if st.button('Add City'):
        flag=0
        flag2=0
        for i in range(len(df)):
            if(df.loc[i]['cityName']==cityName):
                flag=0
                break
            else:
                flag=1
        for i in range(len(df)):
            if((df.loc[i]['lat']==int(lat))&(df.loc[i]['long']==int(long))):
                flag2=0
                break
            else:
                flag2=1
        if flag==1:
            if flag2==1:        
                lat1=int(lat)
                long1=int(long)
                df2 = {'cityName': cityName, 'lat': lat1, 'long': long1}
                df = df.append(df2, ignore_index = True)
                st.write(df)
                df.to_csv('./cities.csv',index = False)
                with st.spinner('Model training for '+cityName+' Please Wait...'):
                    train.trainCity(lat1,long1,cityName)
                st.success(cityName+" added sucessfully !!!")      
            else:
                st.write("Cordinates already exists")
        else:
            st.write("City already exists")
except:
    st.write("error")

