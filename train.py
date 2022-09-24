from cl_data_scraping import data_scrape1
import lstm
import json
from datetime import datetime 
import pandas as pd

def main():
    city=pd.read_csv('cities.csv')
    for i in range(len(city.cityName)):
        #lat,logn,cityName
        data_scrape1(city.lat[i],city.long[i],city.cityName[i])
        lstm.model_train(city.cityName[i])
    a=datetime.now().date()
    data={"last_train_date":str(a)}
    with open("train_time.json", "w") as outfile:
            json.dump(data, outfile)
def trainCity(lat,long,cityName):
    #lat,logn,cityName
    data_scrape1(lat,long,cityName)
    lstm.model_train(cityName)
def train():
   
    try:
        open("train_time.json")
    except:
        main()
    else:
        f = open("train_time.json")
        a=datetime.now().date()
        b = json.load(f)
        if b["last_train_date"] !=str(a):
            main()

train()