
import pandas as pd
import datetime
from dateutil import tz
# importing the requests library
import requests
import json
from datetime import date
import os

def data_scrape1(latI,longI,cityNameI):
    #timezone 
    time_zone= tz.gettz('Asia/Kolkata')
    #time
    from_date = "2/26/2015"
    #to_date = "9/05/2021"
    from_date_format = datetime.datetime.strptime(from_date,
                                            "%m/%d/%Y")
    from_date_format = from_date_format.replace(tzinfo=time_zone)
    print(from_date_format)
    from_unix_time = datetime.datetime.timestamp(from_date_format)
    print(from_unix_time)
    to_date_format = datetime.datetime.now()
    to_date_format = to_date_format.replace(tzinfo=time_zone)
    print(to_date_format)
    to_unix_time = datetime.datetime.timestamp(to_date_format)
    print(to_unix_time)
    def uct2ist(unixIT):
        it=datetime.datetime.utcfromtimestamp(unixIT).strftime('%Y-%m-%d %H:%M:%S')
        it_format = datetime.datetime.strptime(it,
                                                '%Y-%m-%d %H:%M:%S')
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Kolkata')
        it_format = it_format.replace(tzinfo=from_zone)
        ot = it_format.astimezone(to_zone)
        ot=ot.replace(tzinfo=None)
        return(ot)
    print(uct2ist(1606266000))
    URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"
    lat = latI
    lon = longI 
    start =int(from_unix_time)
    end = int(to_unix_time)
    appid = "fdf9bf09f1a8179eb2f4486fead84d21"
    PARAMS = {'lat':lat,'lon':lon,'start':start,'end':end,'appid':appid}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    with open("data_"+cityNameI+".json", "w") as outfile:
        json.dump(data, outfile)
    list=data['list']
    df = pd.DataFrame(columns=['date','no2','so2','pm2_5','pm10'])
    for i in list:
        j=i['components']
        data1 = {
            "date": uct2ist(i['dt']),
            "no2":[j['no2']],
            "so2":j['so2'],
            "pm2_5":j['pm2_5'],
            "pm10":j['pm10'],
            "o3":j['o3'],
            "so2":j['so2'],
            "nh3":j['nh3'],
            "no":j['no']            
        }
        data = pd.DataFrame(data1)
        df = pd.concat([df, data])
    df=df.reset_index()
    df=df.drop(['index'], axis=1)
    os.popen("mkdir data")
    df.to_csv("data/data1_"+cityNameI+".csv",index=False)
    df1 = pd.read_csv("data/data1_"+cityNameI+".csv", parse_dates =["date"], index_col ="date")
    df1=df1.resample('D').mean()
    df1=df1.reset_index()
    df2 = pd.DataFrame(columns=['Date','no2','so2','pm2_5','pm10'])
    for i in range(df1.shape[0]):
        data4 = {
            "Date":df1.loc[i]['date'],
            "no2":[round(df1.loc[i]['no2'],2)],
            "so2":round(df1.loc[i]['so2'],2),
            "pm2_5":round(df1.loc[i]['pm2_5'],2),
            "pm10":round(df1.loc[i]['pm10'],2),
            "o3":round(df1.loc[i]['o3'],2),
            "so2":round(df1.loc[i]['so2'],2),
            "nh3":round(df1.loc[i]['nh3'],2),
            "no":round(df1.loc[i]['no'],2)
        }
        data = pd.DataFrame(data4)
        df2 = pd.concat([df2, data])
    df2=df2.reset_index()
    df2=df2.drop(['index'], axis=1)
    df2.to_csv("data/data_"+cityNameI+".csv", index=False)