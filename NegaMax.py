from OthelloClass import CopyOthello
from Predict import Model
import time


class Negamax:

    def __init__(self,modelname):
        self.model=Model(modelname)
        self.pooled_othello=[]
        self.pooled_node=[]
        self.node_list=[]
        


    def Choose(self,_othello,kaisu_max):
        
        node=Node(_othello,None)

        self.ResetPool()
        t=time.time()
        self.Search(node,kaisu_max)
        if(len(self.pooled_othello)>10**5):
            node=Node(_othello,None)
            self.ResetPool()
            kaisu_max-=1
            self.Search(node,kaisu_max)
        print(len(self.node_list),"個の盤面について探索",format(time.time()-t, '.2f'),"秒")
        t=time.time()
        shoritu_list=self.model.predict(self.pooled_othello)      
        print(len(self.pooled_othello),"個の盤面について推論",format(time.time()-t, '.2f'),"秒")
        # print(len(self.pooled_othello),len(self.node_list))
        for i in range(len(self.pooled_node)):
            self.pooled_node[i].shoritu=shoritu_list[i]
            # print(shoritu_list[i])
        # print(self.pooled_othello[0])
        # for i in range(len(self.node_list)):
        #     print(self.node_list[i].shoritu)
        return self.FindMax(node,kaisu_max)
        

    def FindMax(self,_node,kaisu_max,kaisu=0):
        _othello=_node.othello
        if(kaisu==kaisu_max):
            # return [self.model.predict([_othello])[0],-1]
            return [_node.shoritu,-1]
        # okeru=[]
        # for i in range(64):
        #     if(_othello.canput>>i & 1):
        #         okeru.append(i)
        # if(len(okeru)==0):
        #     okeru=[-1]
        saisho=1
        saiyo=-1
        # for i in range(len(okeru)):
        #     othello=CopyOthello(_othello)
        #     othello.Reverse(okeru[i])
        #     shoritu_aite=self.FindMax(othello,kaisu_max,kaisu+1)[0]
        #     if(shoritu_aite<=saisho):
        #         saiyo=okeru[i]
        #         saisho=shoritu_aite
        for i in range(len(_node.child)):
            shoritu_aite=self.FindMax(_node.child[i],kaisu_max,kaisu+1)[0]
            if(shoritu_aite<=saisho):
                saiyo=_node.child[i].tyokuzen_te
                saisho=shoritu_aite
        _node.shoritu=1-saisho
        return [_node.shoritu,saiyo]

    def Search(self,_node,kaisu_max,kaisu=0):
        if(kaisu==1):print(kaisu)
        _othello=_node.othello
        if(kaisu==kaisu_max):
            self.pooled_node.append(_node)
            self.pooled_othello.append(_othello)
            return
        okeru=[]
        for i in range(64):
            if(_othello.canput>>i & 1):
                okeru.append(i)
        if(len(okeru)==0):
            okeru=[-1]
        for i in range(len(okeru)):
            othello=CopyOthello(_othello)
            othello.Reverse(okeru[i])
            node=Node(othello,okeru[i])
            _node.AddChild(node)
            self.node_list.append(node)
            self.Search(node,kaisu_max,kaisu+1)
        return 


    def ResetPool(self):
        self.pooled_othello=[]
        self.pooled_node=[]
        self.node_list=[]



class Node:
    def __init__(self,othello,tyokuzen):
        self.othello=othello
        self.is_expanded=False
        self.child=[]
        self.shoritu=-1
        self.tyokuzen_te=tyokuzen
        

    def AddChild(self,node):
        self.child.append(node)
        self.is_expanded=True