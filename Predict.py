from OthelloClass import CopyOthello
from Learn4 import Banmen
from Learn4 import Extract

from tensorflow.python.keras.models import load_model
import numpy as np


class Model:

    def __init__(self,_modelname,print_summary=True):
        self.modelnNme=_modelname
        modelPass="Models/"+_modelname+".h5"
        self.model=load_model(modelPass)
        if(print_summary):self.model.summary()

    # def predict(self,_othello):
    #     # othello=Othello(_othello.p,_othello.o)
    #     othello=CopyOthello(_othello)
    #     banmen=Banmen(othello)
    #     isikazu=othello.Count()
    #     okerukazu=othello.GohoCount()
    #     senkyou=[(isikazu[0]-35)/15,(isikazu[1]-35)/15,(okerukazu[0]-5)/5,(okerukazu[1]-5)/5]
    #     # data=[[banmen],[senkyou]]
    #     data=[[senkyou]]
    #     for i in range(10):
    #         data.append([Extract(banmen,i)])
    #     for i in range(len(data)):
    #         data[i]=np.array(data[i])
    #     shouritu=self.model.predict(data)
    #     return shouritu

    def predict(self,othello_lis):
        data=[[]for i in range(11)]
        for i in range(len(othello_lis)):
            othello=CopyOthello(othello_lis[i])
            banmen=Banmen(othello)
            isikazu=othello.Count()
            okerukazu=othello.GohoCount()
            data[0].append([(isikazu[0]-35)/15,(isikazu[1]-35)/15,(okerukazu[0]-5)/5,(okerukazu[1]-5)/5])
            for i in range(10):
                data[i+1].append(Extract(banmen,i))
        for i in range(11):
            data[i]=np.array(data[i])
        result=self.model.predict(data)
        ans=[]
        for i in range(len(result)):
            ans.append(result[i,0])
        
        return ans