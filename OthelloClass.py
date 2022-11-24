from collections import deque
import random


class Othello:
    
    trans = [[1, 8, 0xffffffffffffff00], [1, 7, 0x7f7f7f7f7f7f7f00], [-1, 1, 0x7f7f7f7f7f7f7f7f], [-1, 9, 0x007f7f7f7f7f7f7f],
             [-1, 8, 0x00ffffffffffffff], [-1, 7, 0x00fefefefefefefe], [1, 1, 0xfefefefefefefefe], [1, 9, 0xfefefefefefefe00]]

    def __init__(self, play, oppo,teban=1,hanten=True):

        self.blank = 0x0
        self.canput = 0x0
        self.zen = 0x0
        self.uteru=False
        self.teban = teban
        self.hanten=hanten


        self.p = play
        self.o = oppo
        for i in range(64):
            self.zen |= 1 << i
        self.CanPut()  # CanPutは1秒間に20万回が限界

    def CanPut(self):
        self.blank = self.zen & (~(self.o | self.p))
        ans = 0
        temp = 0
        horizontal = self.o & 0x7e7e7e7e7e7e7e7e
        vertical = self.o & 0x00FFFFFFFFFFFF00
        allside = self.o & 0x007e7e7e7e7e7e00

        # 左
        temp = horizontal & (self.p << 1)
        temp |= horizontal & (temp << 1)
        temp |= horizontal & (temp << 1)
        temp |= horizontal & (temp << 1)
        temp |= horizontal & (temp << 1)
        temp |= horizontal & (temp << 1)
        ans = self.blank & (temp << 1)

        # 右
        temp = horizontal & (self.p >> 1)
        temp |= horizontal & (temp >> 1)
        temp |= horizontal & (temp >> 1)
        temp |= horizontal & (temp >> 1)
        temp |= horizontal & (temp >> 1)
        temp |= horizontal & (temp >> 1)
        ans |= self.blank & (temp >> 1)

        # 上
        temp = vertical & (self.p << 8)
        temp |= vertical & (temp << 8)
        temp |= vertical & (temp << 8)
        temp |= vertical & (temp << 8)
        temp |= vertical & (temp << 8)
        temp |= vertical & (temp << 8)
        ans |= self.blank & (temp << 8)

        # 下
        temp = vertical & (self.p >> 8)
        temp |= vertical & (temp >> 8)
        temp |= vertical & (temp >> 8)
        temp |= vertical & (temp >> 8)
        temp |= vertical & (temp >> 8)
        temp |= vertical & (temp >> 8)
        ans |= self.blank & (temp >> 8)

        # 右上
        temp = allside & (self.p << 7)
        temp |= allside & (temp << 7)
        temp |= allside & (temp << 7)
        temp |= allside & (temp << 7)
        temp |= allside & (temp << 7)
        temp |= allside & (temp << 7)
        ans |= self.blank & (temp << 7)

        # 左上
        temp = allside & (self.p << 9)
        temp |= allside & (temp << 9)
        temp |= allside & (temp << 9)
        temp |= allside & (temp << 9)
        temp |= allside & (temp << 9)
        temp |= allside & (temp << 9)
        ans |= self.blank & (temp << 9)

        # 右下
        temp = allside & (self.p >> 9)
        temp |= allside & (temp >> 9)
        temp |= allside & (temp >> 9)
        temp |= allside & (temp >> 9)
        temp |= allside & (temp >> 9)
        temp |= allside & (temp >> 9)
        ans |= self.blank & (temp >> 9)

        # 左下
        temp = allside & (self.p >> 7)
        temp |= allside & (temp >> 7)
        temp |= allside & (temp >> 7)
        temp |= allside & (temp >> 7)
        temp |= allside & (temp >> 7)
        temp |= allside & (temp >> 7)
        ans |= self.blank & (temp >> 7)

        self.canput = ans

        if(ans!=0):
            self.uteru=True
        else:
            self.uteru=False


    def Reverse(self, _put):
        _put=int(_put)      #_putがnumpy.intだった場合は32桁までしか保持できずにバグの原因となる
        if(_put>=0 and _put<=63):
            put = int(1 << _put)
            rev = 0
            rev_temp = 0
            if ((self.canput & put) == 0):
                raise Exception("不正な手を打ちました")
            for i in range(8):
                rev_temp = 0
                mask = self.Transfer(put, i)
                while((mask != 0) and (mask & self.o) != 0):
                    rev_temp |= mask
                    mask = self.Transfer(mask, i)
                if((mask & self.p) != 0):
                    rev |= rev_temp
            self.p ^= put | rev
            self.o ^= rev
        self.TebanGae()

    def Transfer(self, put, k):
        if(self.trans[k][0] == 1):
            return (put << self.trans[k][1]) & self.trans[k][2]
        if(self.trans[k][0] == -1):
            return (put >> self.trans[k][1]) & self.trans[k][2]

    # def Ranuti(self,kadotori=False):
    def Ranuti(self):
        d = deque()
        # kados=deque()
        for i in range(64):
            if(self.canput>>i & 1):
                d.append(i)
                # if (kadotori and i in [0, 7, 56, 63]):
                #     kados.append(i)
        l = len(d)
        if(l == 0):
            # self.Reverse(-1)
            return [False, -1]
        # elif (len(kados) != 0):
        #     return [True,random.choice(kados)]
        else:
            sentaku = random.randint(0, l-1)
            # self.Reverse(d[sentaku])
            return [True, d[sentaku]]

    def TebanGae(self):
        self.p ^= self.o
        self.o = self.o ^ self.p
        self.p = self.o ^ self.p
        self.teban *= -1
        self.CanPut()

    def Count(self):
        ans = [0, 0]
        num = self.p

        for i in range(2):
            num = num - ((num >> 1) & 0x5555555555555555)

            num = (num & 0x3333333333333333) + ((num >> 2) & 0x3333333333333333)

            num = (num + (num >> 4)) & 0x0f0f0f0f0f0f0f0f 
            num = num + (num >> 8) 
            num = num + (num >> 16)
            num = num + (num >> 32)
            ans[i] = num & 0x0000007f
            num = self.o

        # if(self.teban == -1):
        #     ans[0] ^= ans[1]
        #     ans[1] = ans[0] ^ ans[1]
        #     ans[0] = ans[0] ^ ans[1]
        return ans

    def GohoCount(self):
        ans=[0,0]
        for i in range(2):
            num=self.canput
            num = num - ((num >> 1) & 0x5555555555555555)
            num = (num & 0x3333333333333333) + ((num >> 2) & 0x3333333333333333)
            num = (num + (num >> 4)) & 0x0f0f0f0f0f0f0f0f 
            num = num + (num >> 8) 
            num = num + (num >> 16)
            num = num + (num >> 32)
            ans[i]=num & 0x0000007f
            self.Reverse(-1)
        
        return ans


    def to_64lis(self,num):
        temp=1
        ans=[0]*64
        for i in range(64):
            if((num&temp)!=0):
                ans[63-i]=1
            temp<<=1
        return ans

    # def Hyoji(self):
    #     RED = '\033[31m'
    #     BLUE = '\033[34m'
    #     END = '\033[0m'
    #     PURPLE = '\033[35m'
    #     maru = RED+"○"+END+" "
    #     batu = BLUE+"×"+END+" "
    #     okeru = PURPLE+"."+END+" "
    #     google = True
    #     cmd = True
    #     if(google):
    #         maru = RED+"○"+END
    #         batu = BLUE+"×"+END
    #         okeru = PURPLE+"・"+END
    #     if(cmd):
    #         maru = "○"
    #         batu = "×"
    #         okeru = "・"
    #     print("  a b c d e f g h")
    #     for i in range(8):
    #         retumoji = str(i+1)+" "
    #         for j in range(8):
    #             zurasi = 8*i+j
    #             if((self.p >> zurasi & 1) == 1):
    #                 if(self.teban == 1):
    #                     retumoji += maru
    #                 else:
    #                     retumoji += batu
    #             elif((self.o >> zurasi & 1) == 1):
    #                 if(self.teban == 1):
    #                     retumoji += batu
    #                 else:
    #                     retumoji += maru
    #             elif((self.canput >> zurasi & 1) == 1):
    #                 retumoji += okeru
    #             else:
    #                 if(google):
    #                     retumoji += "ー"
    #                 else:
    #                     retumoji += "--"
    #         print(retumoji)
    #     # print("")

    def __str__(self):
        ans = "  a b c d e f g h"+'\n'
        maru = "○"
        batu = "×"
        okeru = "・"
        kuuhaku="ー"
        kigo=[maru,batu,okeru,kuuhaku]
        if(self.hanten and self.teban==-1):
            kigo[0]=batu
            kigo[1]=maru
        # for i in range(8):
        #     retumoji = str(i+1) + " "
        #     for j in range(8):
        #         zurasi = 8 * i + j
        #         if ((self.p >> zurasi & 1) == 1):
        #             if (self.teban == 1):
        #                 retumoji += maru
        #             else:
        #                 retumoji += batu
        #         elif ((self.o >> zurasi & 1) == 1):
        #             if (self.teban == 1):
        #                 retumoji += batu
        #             else:
        #                 retumoji += maru
        #         elif ((self.canput >> zurasi & 1) == 1):
        #             retumoji += okeru
        #         else:
        #             retumoji += kuuhaku
        #     ans+=retumoji+"\n"
        
        banmen=[self.to_64lis(self.p),self.to_64lis(self.o),self.to_64lis(self.canput),self.to_64lis(self.blank)]
        
        for i in range(8):
            retumoji=str(i+1)+" "
            for j in range(8):
                mada=True
                for k in range(3):
                    if(banmen[k][8*i+j]==1):
                        retumoji+=kigo[k]
                        mada=False
                if(mada):
                    retumoji+=kigo[3]
            ans+=retumoji+"\n"

        return ans
    
def CopyOthello(_othello,teban=2):
    if(teban!=1 and teban!=-1):
        teban=_othello.teban
    return Othello(_othello.p,_othello.o,teban)

if(__name__ == '__main__'):
    kihu="f5f6e6f4e3d6g4d3c3h3c4g3g5g6e7d7h5f3h4h6c6f7c7c5c8d8b5c2d2e2f1f2e8f8g8b3c1b6a4a3b4a5e1d1g7h8h7b8a7a6a2b2a1b1g2g1b7a8h1h2"
    othello=Othello(0x0000000810000000,0x0000001008000000)
    print(othello)

    for i in range(len(kihu)//2):
        if(not othello.uteru):
            othello.Reverse(-1)
            print("Pass")
            print(othello)
        basho=ord(kihu[2*i])-96
        basho=72-int(kihu[2*i+1])*8-basho
        othello.Reverse(basho)
        print(othello)
        print(othello.GohoCount())
        print(othello.Count())