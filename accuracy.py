import pickle

def accuracy(cities):
    acq="Model accuracy for "
    for i in cities:
        with open("./saved_model/lstm_model_"+i+".pkl","rb") as file:
            a=pickle.load(file)
            b=round(a[0],2)
            acq=acq+f"[{i}={b}]"
    return acq
