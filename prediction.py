from lstm import model_prediction
import pandas as pd
from datetime import datetime 
def prediction(a,b,c):
    pollutant=['no2', 'so2', 'pm2_5', 'pm10', 'o3', 'nh3', 'no']
    pollutantValue =0
    for i in range(len(pollutant)):
        if pollutant[i]==c:
            pollutantValue=i
    
    df = pd.DataFrame({
            'Date':pd.date_range(str(datetime.now().date()), periods=b)
        })
    #print(df)
    for i in a:
        #print(i)
        out=model_prediction(i,b,pollutantValue)
        #print(out)
        df1 = pd.DataFrame({
            i:out
        })
        df= pd.concat([df, df1], axis = 1)
        #print(df1)
    #return df.drop('Date',axis=1)
    return df.set_index("Date")
