from distutils.log import error
import time
import streamlit as st
import pandas as  pd
import train
from clear import clear
import yaml
import threading 

import pickle
import streamlit_authenticator as stauth

st.set_page_config(
   page_title="Admin",
   page_icon="🖥️",
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

hashed_passwords = stauth.Hasher(['123', '456']).generate()
with open('./secure.yaml') as file:
    config = yaml.safe_load(file)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])




name, authentication_status, username = authenticator.login('Login to add or remove cities', 'main')

if authentication_status == False:
    st.error("Username or Password is incorrect")
if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.sidebar.title(f"Welcome {name}")
    authenticator.logout('Logout', 'sidebar')
    def register_user():
        try:
                if authenticator.register_user('Register user', preauthorization=False):
                    st.success('User registered successfully')
                    with open('./secure.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    def update_user():
        try:
            if authenticator.update_user_details(username, 'Update user details'):
                st.success('Entries updated successfully')
                with open('./secure.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    def reset_password():
        try:
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
                with open('./secure.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)

        except Exception as e:
            st.error(e)
    def city():
        try:
            dfp=pd.read_csv("./cities_predict.csv")
            dft=pd.read_csv("./cities_train.csv")
            col1,col2,col3,col4 = st.columns(4)
            col1.write("cityName")
            for i in range(len(dfp)):
                col1.write(dfp.loc[i]['cityName'])
            col2.write("latitude")
            for i in range(len(dfp)):
                col2.write(dfp.loc[i]['lat'])
            col3.write("longitude")
            for i in range(len(dfp)):
                col3.write(dfp.loc[i]['long'])
            col4.write("")
            for i in range(len(dfp)):
                if col4.button('Delete',key=i):
                    clear(dfp.loc[i]['cityName'])
                    dfp=dfp.drop(i)     
                    dft=dft.drop(i)
                    dfp.to_csv("./cities_predict.csv", index=False)
                    dft.to_csv("./cities_train.csv", index=False)
            cityName = st.text_input('City Name')
            lat = st.text_input('latitude')
            long = st.text_input('Longitude')

            if st.button('Add City'):
                flag=0
                flag2=0
                for i in range(len(dfp)):
                    if(dft.loc[i]['cityName']==cityName):
                        flag=0
                        break
                    else:
                        flag=1
                for i in range(len(dfp)):
                    if((dft.loc[i]['lat']==int(lat))&(dfp.loc[i]['long']==int(long))):
                        flag2=0
                        break
                    else:
                        flag2=1
                if flag==1:
                    if flag2==1:        
                        lat1=int(lat)
                        long1=int(long)
                        df2 = {'cityName': cityName, 'lat': lat1, 'long': long1}
                        dft = dft.append(df2, ignore_index = True)
                        dfp=dfp.append(df2,ignore_index = True)
                        st.write(dft)
                        dft.to_csv('./cities_train.csv',index = False)
                        def add_city_train():
                            train.trainCity(lat1,long1,cityName)
                            dfp.to_csv('./cities_predict.csv',index = False)   
                        with st.spinner('Model training for '+cityName+' Please Wait...'):
                            t2 = threading.Thread(target=add_city_train)
                            t2.start() 
                        st.success(f"Model for {cityName} will be added soon")
                    else:
                        st.write("Cordinates already exists")
                else:
                    st.write("City already exists")
        except:
            st.write("error")


    page_names_to_funcs = {
    "Cities":city,
    "Register User": register_user,
    "Reset Password": reset_password,
    "Update User": update_user,
}
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()
    
