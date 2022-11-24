import math
from multiprocessing import pool
import random
import time
# from OthelloClass import Othello
from OthelloClass import CopyOthello
from Predict import Model

class Node:
    def __init__(self,othello,tyokuzen=-1):
        self.othello=othello
        self.is_expanded=False
        self.finished=False
        self.child=[]
        self.playout_num=0
        self.win_point=0 #勝利＋１ 引き分け0 敗北-1
        self.tyokuzen_te=tyokuzen
        self.expand_min=10  #この回数以上プレイアウトしてたら展開する

        self.hugeNum=10000
        

    def AddChild(self,node):
        self.child.append(node)
        self.is_expanded=True

    def Expand(self):
        if(self.is_expanded):
            return
        if(self.othello.canput==0):
            copyOthello=CopyOthello(self.othello)
            copyOthello.Reverse(-1)
            if(copyOthello.canput==0):
                self.finished=True
                return
            self.AddChild(Node(copyOthello,-1))
            return
        for i in range(64):
            if(self.othello.canput>>i & 1):
                copyOthello=CopyOthello(self.othello)
                copyOthello.Reverse(i)
                self.AddChild(Node(copyOthello,i))

    def PlayOut(self):
        self.playout_num+=1
        if(not self.is_expanded and self.playout_num>self.expand_min and not self.finished):
            self.Expand()
        result=[]
        teban=1
        if(self.is_expanded):
            saidai=-10000
            sentaku=None
            yet_play=[]
            for c in self.child:
                hyoka=self.Calc(c)
                if(hyoka>saidai):
                    saidai=hyoka
                    sentaku=c
                if(hyoka==self.hugeNum):
                    yet_play.append(c)
            if(len(yet_play)):
                sentaku=random.choice(yet_play)
            result=sentaku.PlayOut()
            teban=-1
        else:
            copyOthello=CopyOthello(self.othello,1)
            for i in range(150):
                if(copyOthello.canput==0):
                    copyOthello.Reverse(-1)
                    if(copyOthello.canput==0):
                        break
                copyOthello.Reverse(copyOthello.Ranuti()[1])
            result=copyOthello.Count()
            teban=copyOthello.teban
        if(teban==-1):
            result[0]^=result[1]
            result[1]^=result[0]
            result[0]^=result[1]
        self.Add(result)
        return result
            
    def Add(self,result):
        if(result[0]>result[1]):
            self.win_point+=1
        if(result[0]<result[1]):
            self.win_point-=1
        return



    def Calc(self,c):
        if(c.playout_num==0):
            return self.hugeNum
        ans=0.5-c.win_point/c.playout_num/2
        ans+=math.sqrt(2*math.log(self.playout_num)/c.playout_num)
        return ans



class Monte:
    def __init__(self,namae):
        self.model=Model(namae)


    def MonteSearch(self,_othello,jikan_max=5):
        othello=CopyOthello(_othello)
        root=Node(othello)
        # root.Expand()
        self.Search(root)
        t=time.time()
        monte_cnt=0
        for i in range(10**8):
            if(time.time()-t>jikan_max):
                break
            monte_cnt+=1
            root.PlayOut()
        saidai=-1
        for c in root.child:
            if(c.playout_num>saidai):
                saidai=c.playout_num
                sentaku=c.tyokuzen_te

        result_print = []
        alphabets = ['Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ']
        sujis=['１','２','３','４','５','６','７','８']
        for c in root.child:
            if(c.playout_num==0):
                continue
            basho=c.tyokuzen_te
            kaisu="{0:6}".format(c.playout_num)
            shouritu="{0:6.2f}".format(50-50*c.win_point/c.playout_num)
            result_print.append(alphabets[7-basho%8]+sujis[7-basho//8]+"に置いた場合 試行回数："+kaisu+"   勝率："+shouritu)
        if(len(result_print)):
            result_print.sort()
        for r_p in result_print:
            print(r_p)
        return sentaku


    def Search(self,root):
        pooled_node=[root]
        pooled_othelllo=[root.othello]
        list_max=10**4
        t=time.time()
        for i in range(list_max):
            len_now=len(pooled_node)
            if(i>=len_now or len_now>list_max):
                break
            pooled_node[i].Expand()
            if(pooled_node[i].finished):
                continue
            for c in pooled_node[i].child:
                pooled_node.append(c)
                pooled_othelllo.append(c.othello)
        print("盤面の探索終わり",format(time.time()-t, '.2f'),"秒") 
        t=time.time()
        pooled_shoritu=self.model.predict(pooled_othelllo)
        print(len(pooled_shoritu),"個の盤面について推論",format(time.time()-t, '.2f'),"秒")
        for i in range(len(pooled_node)):
            count_now=pooled_othelllo[i].Count()
            isi_sum=count_now[0]+count_now[1]
            kaisu=min(64-isi_sum,40)*50
            pooled_node[i].playout_num+=kaisu
            pooled_node[i].win_point+=int((pooled_shoritu[i]*2-1)*(kaisu+1))