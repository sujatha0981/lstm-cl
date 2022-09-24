import os
def clear(cityName):
    os.remove("data_"+cityName+".json")
    os.remove("data/data1_"+cityName+".csv")
    os.remove("data/data_"+cityName+".csv")
    os.remove('saved_model/lstm_model_'+cityName+'.h5')

