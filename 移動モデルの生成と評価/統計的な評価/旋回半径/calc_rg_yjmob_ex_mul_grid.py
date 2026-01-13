import fractions
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
import shutil
import re

#
#z1---------z2
#|           |
#|           |
#|           |
#|           |
#z3---------z4
  
#z=[35.66, 139.97, 35.72, 140.03] #tkb
#z=[37.55, -122.57,37.85, -122.27] #taxi
z=[1.00, 1.00,200.00, 200.00]   #data_yjmob
delta = z[2]-z[0]
apart=40

xapart=[]
yapart=[]

grid=np.zeros([apart,apart])

trajectory_x=[]
trajectory_y=[]


os.chdir(os.path.dirname(os.path.abspath(__file__)))

effective_digits1 = 6
effective_digits2 = 2


def import_data_start(l_name, f_name):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name)
    cur = con.cursor()
    cur.execute('SELECT startpos FROM '+str(l_name)+' WHERE id BETWEEN 150000 and 500000')
    a=cur.fetchall()
    return a

def import_data_goal(l_name, f_name):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name)
    cur = con.cursor()
    cur.execute('SELECT goalpos FROM '+str(l_name)+' WHERE id BETWEEN 150000 and 500000')
    b=cur.fetchall()
    return b


if __name__ == '__main__':
    pass

    for uid in range(0,21):

        x_list=[]
        y_list=[]

        file_name = 'main/main_yjmob_uid'+str(uid)+'_irl200_ep500000.db'

        try:
            data_start=import_data_start("expart",file_name)
            data_goal=import_data_goal("expart",file_name)
        except:
            continue

        for i in range (len(data_start)):
            pattern1 = r'(-?\d+), (-?\d+)'
            data=re.search(pattern1, str(data_start[i]))
            x_list.append(data.group(1))
            y_list.append(data.group(2))


        for i in range(apart):
            xapart.append(round(z[0]+delta/apart*i, 4))
            yapart.append(round(z[1]+delta/apart*i, 4))


        for j in range(len(x_list)):
            x=y=int()
            #print(latitude_list[j])
            if (x_list[j]<=z[2]) and (z[0]<=x_list[j]) and  (y_list[j]<=z[3]) and (z[1]<=y_list[j]):
                #print(1)
                for x in range(apart):
                    #print(x)
                    if x_list[j]<=xapart[x]:
                        break

                for y in range(apart):
                    if y_list[j]<=yapart[y] :
                        break

                #print(x,y)
                    
                if grid[apart-x][y]<=1000:
                    grid[apart-x][y]+=1 
                    trajectory_x.append(round(x_list[j], effective_digits1))
                    trajectory_y.append(round(y_list[j], effective_digits1))




        # 格納
        trace_list = []
        trace_list.append( ( round(((z[0])+((delta/apart) * round(float(trajectory_x[0]), effective_digits2))), effective_digits2), round(((z[1])+((delta/apart) * round(float(trajectory_y[0]), effective_digits2))), effective_digits2) ) )  
        for i in range(1,len(x_list)-1):
            if ( trajectory_x[i-1]!=trajectory_x[i] ) and ( trajectory_y[i-1]!=trajectory_y[i] ):
                trace_list.append( ( round(((z[0])+((delta/apart) * round(float(trajectory_x[i]), effective_digits2))), effective_digits2), round(((z[1])+((delta/apart) * round(float(trajectory_y[i]), effective_digits2))), effective_digits2) ) )  


        # 重心計算
        cm_lat = 0
        cm_lon = 0
        r_cm = []
        for i in range (len(trace_list)):
            cm_lat += trace_list[i][0]
            cm_lon += trace_list[i][1]

        try:
            cm_lat = cm_lat / float(len(trace_list))
            cm_lon = cm_lon / float(len(trace_list))
        except:
            continue
    
        r_cm = [cm_lat, cm_lon]


        # 旋回半径の抽出
        R_g = 0.0
        for i in range(len(trace_list)):
            R_g += (trace_list[i][0] - r_cm[0])**2 + (trace_list[i][1] - r_cm[1])**2
        R_g = np.sqrt(R_g / float(len(trace_list)))


        # 旋回半径計算
        # k(=2)-旋回半径(移動半径) r_g^{(k)} の計算
        frequency_dict = {}
        sorted_frequency_dict = []
        for i in range (len(trace_list)):
            if trace_list[i] not in frequency_dict.keys():
                frequency_dict[ trace_list[i] ] = 1
            else :
                frequency_dict[ trace_list[i] ] += 1   
        sorted_frequency_dict = sorted(frequency_dict.items(), key=lambda x:x[1], reverse=True)

        R_g2_cm_lat = 0
        R_g2_cm_lon = 0
        R_g2_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0]) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1])
        R_g2_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1]) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1])

        # r_g^{(2)}
        R_g2 = 0
        R_g2 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g2_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g2_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g2_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g2_cm_lon)**2 ))
        R_g2 = np.sqrt(R_g2/float(sorted_frequency_dict[0][1]+sorted_frequency_dict[1][1]))

        # S2
        s2 = 0
        s2 = (R_g2)/(R_g)
        print(s2)


        # k(=4)-旋回半径(移動半径) r_g^{(k)} の計算
        # R_g4
        try:
            R_g4_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0]) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1])
            R_g4_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1]) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1])

            # r_g^{(4)}
            R_g4 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g4_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g4_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g4_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g4_cm_lon)**2 ))
            R_g4 = np.sqrt(R_g4/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1]))

            # s4
            s4 = (R_g4)/(R_g)
        
        except:
            print("uid:"+str(uid)+"のRg4はなし")    


        # k(=6)-旋回半径(移動半径) r_g^{(k)} の計算
        # R_g6
        try:
            R_g6_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][0] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][0] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1])
            R_g6_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][1] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][1] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1])

            # r_g^{(6)}
            R_g6 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[4][1] * ( (sorted_frequency_dict[4][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[4][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[5][1] * ( (sorted_frequency_dict[5][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[5][0][1] - R_g6_cm_lon)**2 ))
            R_g6 = np.sqrt(R_g6/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1]))

            # s6
            s6 = (R_g6)/(R_g)

        except:
            print("uid:"+str(uid)+"のRg6はなし")

        # k(=8)-旋回半径(移動半径) r_g^{(k)} の計算
        # R_g8
        try:
            R_g8_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][0] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][0] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][0] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][0] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1])
            R_g8_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][1] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][1] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][1] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][1] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1])

            # r_g^{(8)}
            R_g8 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[4][1] * ( (sorted_frequency_dict[4][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[4][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[5][1] * ( (sorted_frequency_dict[5][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[5][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[6][1] * ( (sorted_frequency_dict[6][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[6][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[7][1] * ( (sorted_frequency_dict[7][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[7][0][1] - R_g8_cm_lon)**2 ))
            R_g8 = np.sqrt(R_g8/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1]))

            # s8
            s8 = (R_g8)/(R_g)

        except:
            print("uid:"+str(uid)+"のRg8はなし")


        # k(=10)-旋回半径(移動半径) r_g^{(k)} の計算
        # R_g10
        try:
            R_g10_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][0] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][0] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][0] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][0] + sorted_frequency_dict[8][1] * sorted_frequency_dict[8][0][0] + sorted_frequency_dict[9][1] * sorted_frequency_dict[9][0][0] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1] + sorted_frequency_dict[8][1] + sorted_frequency_dict[9][1])
            R_g10_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][1] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][1] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][1] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][1] + sorted_frequency_dict[8][1] * sorted_frequency_dict[8][0][1] + sorted_frequency_dict[9][1] * sorted_frequency_dict[9][0][1] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1] + sorted_frequency_dict[8][1] + sorted_frequency_dict[9][1])

            # r_g^{(10)}
            R_g10 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[4][1] * ( (sorted_frequency_dict[4][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[4][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[5][1] * ( (sorted_frequency_dict[5][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[5][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[6][1] * ( (sorted_frequency_dict[6][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[6][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[7][1] * ( (sorted_frequency_dict[7][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[7][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[8][1] * ( (sorted_frequency_dict[8][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[8][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[9][1] * ( (sorted_frequency_dict[9][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[9][0][1] - R_g10_cm_lon)**2 ))
            R_g10 = np.sqrt(R_g10/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1] + sorted_frequency_dict[8][1] + sorted_frequency_dict[9][1]))

        #s10
            s10 = (R_g10)/(R_g)
        except:
            print("uid:"+str(uid)+"のRg10はなし")

        # ファイルに出力

        f = open('result/rg_yjmob_uid'+str(uid)+'_irl200_ep500000.txt', 'w')
        f.write("uid:"+str(uid))
        f.write('\n'+"R_cm = "+str(r_cm))
        f.write('\n'+"R_g = "+str(R_g))
        f.write('\n'+"R_g2 = "+str(R_g2))
        try:
            f.write('\n'+"R_g4 = "+str(R_g4))
            f.write('\n'+"R_g6 = "+str(R_g6))
            f.write('\n'+"R_g8 = "+str(R_g8))
            f.write('\n'+"R_g10 = "+str(R_g10))
        except:
            print("uid:"+str(uid)+"のRg記載なし")


        f.write('\n'+"s2 = "+str(s2))
        try:
            f.write('\n'+"s4 = "+str(s4))
            f.write('\n'+"s6 = "+str(s6))
            f.write('\n'+"s8 = "+str(s8))
            f.write('\n'+"s10 = "+str(s10))
        except:
            print("uid:"+str(uid)+"のS記載なし")

        f.close()

        f = open('result/freq_yjmob_uid'+str(uid)+'_irl200_ep500000.txt', 'w')
        f.write("uid:"+str(uid))
        f.write('\n'+"学習後の訪問頻度1番目から10番目:")
        f.write('\n'+"1番目:"+str(sorted_frequency_dict[0]))
        f.write('\n'+"2番目:"+str(sorted_frequency_dict[1]))
        try:
            f.write('\n'+"3番目:"+str(sorted_frequency_dict[2]))
            f.write('\n'+"4番目:"+str(sorted_frequency_dict[3]))
            f.write('\n'+"5番目:"+str(sorted_frequency_dict[4]))
            f.write('\n'+"6番目:"+str(sorted_frequency_dict[5]))
            f.write('\n'+"7番目:"+str(sorted_frequency_dict[6]))
            f.write('\n'+"8番目:"+str(sorted_frequency_dict[7]))
            f.write('\n'+"9番目:"+str(sorted_frequency_dict[8]))
            f.write('\n'+"10番目:"+str(sorted_frequency_dict[9]))
        except:
            print("uid:"+str(uid)+"のRg記載なし")
        f.close()

