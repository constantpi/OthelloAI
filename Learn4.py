
from OthelloClass import Othello
from OthelloClass import CopyOthello
import csv

import tensorflow as tf
import tensorflow.keras

# もし入っていない場合はエラーが出ます（何もエラーが出なければOK）
import numpy as np 

from tensorflow.keras.layers import Input #ニューラルネットワークの入力に用いる
from tensorflow.keras.layers import Dense #ニューラルネットワークの各層の変換に用いる（Dense: 通常の層（全結合層）を意味する）
from tensorflow.keras.models import Model #ニューラルネットワークモデル構築に用いる
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten #畳み込み・プーリング・ベクトル化を読み込み
from tensorflow.keras.layers import concatenate
from tensorflow.keras.layers import BatchNormalization,Activation
from tensorflow.python.keras.models import load_model


gamma=0.98

# focus=[[0,1,2,3,8,9,10,16,17,24],\
#     [4,5,6,7,13,14,15,22,23,31],\
#     [32,40,41,48,49,50,56,57,58,59],\
#     [39,46,47,53,53,55,60,61,62,63],\
#     [0,1,2,3,4,5,6,7,9,14],\
#     [0,8,16,24,32,40,48,56,9,49],\
#     [56,57,58,59,60,61,62,63,49,54],\
#     [7,15,23,31,39,47,55,63,14,54],\
#     [0,9,18,27,36,45,54,63],\
#     [7,14,21,28,35,42,49,56]]

focus=[[0,1,2,3,8,9,10,16,17,24],\
    [4,5,6,7,13,14,15,22,23,31],\
    [32,40,41,48,49,50,56,57,58,59],\
    [39,46,47,53,53,55,60,61,62,63],\
    [0,1,2,3,4,5,6,7],\
    [0,8,16,24,32,40,48,56],\
    [56,57,58,59,60,61,62,63],\
    [7,15,23,31,39,47,55,63],\
    [0,9,18,27,36,45,54,63],\
    [7,14,21,28,35,42,49,56]]

def Banmen(_othe):
    # othe=Othello(_othe.p,_othe.o)
    othe=CopyOthello(_othe)
    jibun=othe.to_64lis(othe.p)
    jibun_okeru=othe.to_64lis(othe.canput)
    othe.Reverse(-1)
    aite=othe.to_64lis(othe.p)
    aite_okeru=othe.to_64lis(othe.canput)
    ans=[[[0,0,0,0] for j in range(8)] for i in range(8)]
    for i in range(64):
        if(jibun[i]):
            ans[i//8][i%8][0]=1
        if(aite[i]):
            ans[i//8][i%8][1]=1
        if(jibun_okeru[i]):
            ans[i//8][i%8][2]=1
        if(aite_okeru[i]):
            ans[i//8][i%8][3]=1
    return ans

def Extract(banmen,bango):
    ans=[]
    for i in range(len(focus[bango])):
        basho=focus[bango][i]
        for j in range(4):
            ans.append(banmen[basho//8][basho%8][j])
    return ans





if(__name__ == '__main__' ):
    debug=False

    count_data=[]
    kado_data=[[] for i in range(4)]
    hen_data=[[]for i in range(6)]
    y_data=[]

    testYear=2021
    testYear=2022
    trainNum=0
    # year_list=[2013,2014,testYear]
    year_list=[2016,testYear]
    for year in year_list:

        print("\n"+str(year))

        if(year==testYear):
            trainNum=len(y_data)

        fileName="OthelloData\OfficialRecord\wthor_"+str(year)+".csv"
        datafile = open(fileName, 'r', encoding='utf-8')
        dataReader = csv.reader(datafile)
        cnt=-1


        for row in dataReader:
            one_game=[]
            hyoka=[]
            senkyou=[]
            cnt+=1
            if(cnt==0):continue
            if(debug and cnt==2):
                break

            if(cnt%100==0):
                print(cnt,end=" ")
                # if(cnt==300):break

            

        

            kihu=row[8]
            # print(kihu)
            othello=Othello(0x0000000810000000,0x0000001008000000)
            
            i=0
            while(i<len(kihu)//2):
                basho=ord(kihu[2*i])-96
                basho=72-int(kihu[2*i+1])*8-basho
                if(not othello.uteru):
                    basho=-1
                    i-=1
                i+=1
                othello.Reverse(basho)
                one_game.append(Banmen(othello))
                hyoka.append(None)
                isikazu=othello.Count()
                okerukazu=othello.GohoCount()
                senkyou.append([(isikazu[0]-35)/15,(isikazu[1]-35)/15,(okerukazu[0]-5)/5,(okerukazu[1]-5)/5])
                if(debug):
                    print(othello)
                    print(othello.GohoCount())
                    print(othello.Count())
                    print(one_game[-1])
            banmen_kazu=len(hyoka)
            kekka=othello.Count()
            if(kekka[0]<kekka[1]):
                hyoka[-1]=-1
            elif(kekka[0]>kekka[1]):
                hyoka[-1]=1
            else:
                hyoka[-1]=0
            for i in range(1,banmen_kazu):
                hyoka[banmen_kazu-i-1]=-gamma*hyoka[banmen_kazu-i]
            for k in range(1,banmen_kazu):
                shoritu=(1+hyoka[k])/2
                for t in range(8):
                    kaiten=[[]for i in range(8)]
                    for i in range(8):
                        for j in range(8):
                            n=i
                            m=j
                            if(t&4):
                                m=i
                                n=j
                            if(t&2):
                                n=7-n
                            if(t&1):
                                m=7-m
                            kaiten[i].append(one_game[k][n][m])
                    count_data.append(senkyou[k])
                    y_data.append(shoritu)
                    for i in range(4):
                        kado_data[i].append(Extract(kaiten,i))
                    for i in range(6):
                        hen_data[i].append(Extract(kaiten,i+4))
            
        datafile.close()


    print("ReadFinished")

    # b=banmen_train[-1]
    # for bb in b:
    #     print(bb)
    # print("\n\n")
    # for k in range(10):
    #     print(Extract(b,k))


    # print(count_train)
    # print(banmen_train[0],y_train[0])

    allData=[count_data]


    for i in range(4):
        allData.append(kado_data[i])
    for i in range(6):
        allData.append(hen_data[i])

    trainData=[]
    testData=[]
    for i in range(len(allData)):
        trainData.append(allData[i][:trainNum])
        testData.append(allData[i][trainNum:])
        trainData[i]=np.array(trainData[i])
        testData[i]=np.array(testData[i])

    y_data=np.array(y_data)
    y_train=y_data[:trainNum]
    y_test=y_data[trainNum:]

    print("CopyFinished")

    print("TrainData")
    for i in range((len(trainData))):
        print(trainData[i].shape,end=" ")
    print(y_train.shape)
    print("TestData")
    for i in range(len(testData)):
        print(testData[i].shape,end=" ")
    print(y_test.shape)

    input_banmen_shape=(8,8,4)
    kernel_size=(4,4)
    num_filters=10





    # input_banmen=Input(shape=input_banmen_shape,name="Input_banmen")
    # middle1=Conv2D(num_filters,kernel_size=kernel_size,activation='relu',padding="same",name="1st_Conv")(input_banmen)
    # middle1=MaxPooling2D(pool_size=(2,2))(middle1)
    # middle2=Flatten()(middle1)

    input_count=Input(shape=(4),name="Input_count")


    Inputs=[input_count]

    # middle=Dense(10)(input_count)
    # middle=Activation("relu")(middle)
    # middle=Dense(10)(middle)
    # middle=Activation("relu")(middle)


    Middles=[input_count]
    # Middles=[middle]

    extractShape=[]
    extractInputName=[]
    for i in range(4):
        extractShape.append(40)
        extractInputName.append("Kado"+str(i+1))
    for i in range(6):
        extractShape.append(32)
        extractInputName.append("Hen"+str(i+5))

    for i in range(10):
        x=Input(shape=(extractShape[i]),name="Input"+extractInputName[i])
        Inputs.append(x)
        # x=Dense(10,name="Dense1"+extractInputName[i])(x)
        # x=BatchNormalization()(x)
        # x=Activation("relu")(x)
        x=Dense(extractShape[i],name="Dense1"+extractInputName[i],activation="relu")(x)
        # x=BatchNormalization()(x)
        # x=Activation("relu")(x)
        x=Dense(1,name="Dense2"+extractInputName[i],activation="relu")(x)
        # x=Dense(4,activation="relu",name="Dense2"+extractInputName[i])(x)
        Middles.append(x)
    combined=concatenate(Middles)
    # x=Dense(100,activation="relu")(combined)
    # x=Dense(100,activation="relu")(x)
    # x=Dense(10,activation="relu")(x)
    x=Dense(100,activation="relu")(combined)
    # x = BatchNormalization()(x)
    # x = Activation('relu')(x)
    x=Dense(100,activation="relu")(x)
    # x = BatchNormalization()(x)
    # x = Activation('relu')(x)
    x=Dense(10,activation="relu")(x)
    # x = BatchNormalization()(x)
    # x = Activation('relu')(x)
    output=Dense(1,activation="sigmoid")(x)



    CNN_model=tensorflow.keras.Model(inputs=Inputs,outputs=output)
    

    CNN_model.compile(loss="mse",optimizer=tf.keras.optimizers.Adam(),metrics=['mse'])

    # CNN_model=load_model("Models/Predict08132130.h5")
    CNN_model=load_model("Predict.h5")
    CNN_model.summary()

    epochs=10
    # history=CNN_model.fit([banmen_train,count_train],y_train,batch_size=64,epochs=epochs,verbose=1,validation_split=0.2)

    packsize=100000
    print()
    for i in range(trainData[0].shape[0]//packsize):
        trainPack=[]
        for j in range(len(trainData)):
            trainPack.append(trainData[j][i*packsize:(i+1)*packsize])
            
            
        # history=CNN_model.fit(trainData[i*packsize:(i+1)*packsize],y_train[i*packsize:(i+1)*packsize],batch_size=64,epochs=epochs,verbose=1,validation_split=0.2)
        history=CNN_model.fit(trainPack,y_train[i*packsize:(i+1)*packsize],batch_size=64,epochs=epochs,verbose=1,validation_split=0.2)

        CNN_model.save('Predict.h5')

        test_scores=CNN_model.evaluate(testData,y_test)

