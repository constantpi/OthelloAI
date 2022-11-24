from math import fabs
from OthelloClass import Othello
from NegaMax import Negamax
from MCTS import Monte

import random



dict={}
for i in range(64):
    dict[chr(104-i%8)+str(8-i//8)]=i

shote=["d3","c4","f5","e6"]
othello=Othello(0x0000000810000000,0x0000001008000000)
if(random.randrange(2)):
    othello.Reverse(dict[shote[random.randrange(4)]])


# nega=Negamax("Predict08140214")
# nega=Negamax("Predict08141311")
# monte=Monte("Predict08141311")

nega=Negamax("Predict08192150")
monte=Monte("Predict08192150")

passed=False
turn=1

human=input("あなたが対戦しますか？[yes?]")=="yes"

# for i in range(100):
#     print(othello)
#     if(passed and othello.canput==0):
#         break
#     if(othello.canput==0):
#         othello.Reverse(-1)
#         passed=True
#         turn=1-turn
#         continue
    
#     if(turn):
#         basho=64
#         while((othello.canput>>basho & 1)==0):
#             sentaku=""
#             while(not sentaku in dict):
#                 sentaku=input("どこに打ちますか？")
#             basho=dict[sentaku]
#     else:
#         basho=-1
#         if(othello.GohoCount()[0]-1):
#             result=nega.Choose(othello,5)
#             print(result)
#             basho=result[1]
#             print(chr(104-basho%8)+str(8-basho//8))
#             basho=MonteSearch(othello)
#             print(basho)
#             print(chr(104-basho%8)+str(8-basho//8))

#         else:
#             for i in range(64):
#                 if(othello.canput>>i & 1):
#                     basho=i
#     othello.Reverse(basho)
#     passed=False
#     turn=1-turn


for i in range(100):
    print(othello)
    totyu=othello.Count()
    if(othello.teban==-1):
        totyu=[totyu[1],totyu[0]]
    print(totyu)
    # input()
    if(passed and othello.canput==0):
        break
    if(othello.canput==0):
        othello.Reverse(-1)
        passed=True
        turn=1-turn
        continue
    
    if(turn):
        if(human):
            basho=64
            while((othello.canput>>basho&1)==0):
                sentaku=""
                while(not sentaku in dict):
                    sentaku=input("どこに打ちますか？")
                basho=dict[sentaku]
        else:
            basho=-1
            if(othello.GohoCount()[0]-1):
                result=nega.Choose(othello,5)
                print(result)
                basho=result[1]
                print(chr(104-basho%8)+str(8-basho//8))
            else:
                for i in range(64):
                    if(othello.canput>>i & 1):
                        basho=i
    else:
        basho=-1
        if(othello.GohoCount()[0]-1):
            # basho=MonteSearch(othello)
            basho=monte.MonteSearch(othello)
            print(basho)
            print(chr(104-basho%8)+str(8-basho//8))

        else:
            for i in range(64):
                if(othello.canput>>i & 1):
                    basho=i
    othello.Reverse(basho)
    passed=False
    turn=1-turn