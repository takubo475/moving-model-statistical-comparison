import math
import numpy as np
import sys

import matplotlib.pyplot as plt

import os
import shutil
import re

import seaborn as sns
import scipy

from collections import Counter
from math import log2


os.chdir(os.path.dirname(os.path.abspath(__file__)))

effective_digits = 2

id_start = int(0)
id_end= int(400)


#
#z1---------z2
#|           |
#|           |
#|           |
#|           |
#z3---------z4

z=[0.00, 0.00,200.00, 200.00]   #data_yjmob
delta=(z[2]-z[0])
apart=40

def entropy_from_counter(counter):
    #""" シャノンエントロピー"""
    total = sum(counter.values())
    if total == 0:
        return 0.0
    probs = [c / total for c in counter.values()]
    return -sum(p * log2(p) for p in probs if p > 0)

def sunc_xy(x_list, y_list):
    #""" 非時間相関エントロピー"""
    counter_xy = Counter(zip(x_list, y_list))
    return entropy_from_counter(counter_xy)

def srand_xy(x_list, y_list):
    #""" ランダムエントロピー"""
    L = len(set(zip(x_list, y_list)))
    return log2(L) if L > 0 else 0.0

def import_data(l_name1,f_name1):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name1)
    cur = con.cursor()
    cur.execute('SELECT latitudeE7, longitudeE7 FROM '+str(l_name1))
    aa=cur.fetchall()
    bb = len(aa)
    return aa, bb


def import_dmain_start(l_name2, f_name2):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name2)
    cur = con.cursor()
    cur.execute('SELECT startpos FROM '+str(l_name2)+' WHERE id BETWEEN 150000 and 300000')
    cc=cur.fetchall()
    dd = len(cc)
    return cc, dd

def import_dmain_goal(l_name3, f_name3):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name3)
    cur = con.cursor()
    cur.execute('SELECT goalpos FROM '+str(l_name3)+' WHERE id BETWEEN 150000 and 300000')
    ee=cur.fetchall()
    ff = len(ee)
    return ee, ff


def import_data_time(l_name4, f_name4):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name4)
    cur = con.cursor()
    cur.execute('SELECT hour FROM '+str(l_name4))
    gg=cur.fetchall()
    hh = len(gg)
    return gg, hh


def import_data_minutes(l_name5, f_name5):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name5)
    cur = con.cursor()
    cur.execute('SELECT goalpos FROM '+str(l_name5))
    ii=cur.fetchall()
    jj = len(ii)
    return ii, jj


def import_dmain_step(l_name6, f_name6):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name6)
    cur = con.cursor()
    cur.execute('SELECT step FROM '+str(l_name6)+' WHERE id BETWEEN 150000 and 300000')
    kk=cur.fetchall()
    ll = len(kk)
    return kk, ll





if __name__ == '__main__':
    pass


    S_rand_list1=[]
    S_unc_list1=[]
    S_real_list1=[]

    S_rand_list2=[]
    S_unc_list2=[]
    S_real_list2=[]

    for uid in range(id_start,id_end+1):

        x1=[]
        x2=[]
        y1=[]
        y2=[]
        t1=[]
        t2=[]
        s2=[]
        dis_list1 = []
        dis_list2 = []
        timecount=0
        minutecount=0
        

    
        file_name1 = 'data/data_yjmob_B'+str(uid)+'.db'
        file_name2 = 'main/main_yjmob_uid'+str(uid)+'_irl200_ep500000.db'

        ## dataのほう,準備
        try:
            data1, dr1=import_data("expart",file_name1)
            time1, minute1=import_data_time("expart",file_name1)
        except:
            continue



        for i in range (len(data1)):
        
            pattern1 = r'(-?\d+), (-?\d+)'
            d_text1=re.search(pattern1, str(data1[i]))
            x1.append(round(float(d_text1.group(1)), effective_digits))
            y1.append(round(float(d_text1.group(2)), effective_digits))


        for i in range (len(time1)):
            pattern1 = r'(-?\d+),'
            d_text2=re.search(pattern1, str(time1[i]))
            t1.append(round(float(d_text2.group(1)), effective_digits))




        ##  mainのほう,準備
        try:
            dmain_start, dr2=import_dmain_start("expart",file_name2)
            dmain_goal, dr3=import_dmain_goal("expart",file_name2)
            dmain_step, dr4=import_dmain_step("expart",file_name2)
        except:
            continue




        for i in range (len(dmain_start)):
            if dmain_start[i] != dmain_goal[i]:
                pattern1 = r'(-?\d+), (-?\d+)'
                pattern2 = r'(-?\d+),'
                d_text2=re.search(pattern1, str(dmain_start[i]))
                x2.append(((z[0])+((delta/apart) * ((round(float(d_text2.group(1)), effective_digits))))))
                y2.append(((z[1])+((delta/apart) * ((round(float(d_text2.group(2)), effective_digits))))))

                d_text3=re.search(pattern2, str(dmain_step[i]))
                s2.append(round(float(d_text3.group(1)), effective_digits))

        for i in range (len(s2)):
            minutecount+=s2[i]

            if minutecount>=60.0:
                minutecount-=60.0
                timecount+=1

            if timecount>=24:
                timecount-=24

            t2.append(timecount)

    
        trace_list1 = []
        trace_list2 = []

        for i in range(len(x1)-2):
            trace_list1.append((x1[i],y1[i],t1[i],x1[i+1],y1[i+1],t1[i+1],x1[i+2],y1[i+2],t1[i+2]))


        for i in range(len(x2)-2):
            trace_list2.append((x2[i],y2[i],t2[i],x2[i+1],y2[i+1],t2[i+1],x2[i+2],y2[i+2],t2[i+2]))


        if (len(trace_list1)==0)or(len(trace_list2)==0):
            continue


        # --- data 側（expart） ---
        # Sreal
        counter1 = Counter(trace_list1)  # (x1,y1,t1,x2,y2,t2)
        total1 = sum(counter1.values())
        if total1 > 0:
            probs1 = (c / total1 for c in counter1.values())
            S1_real = -sum(p * log2(p) for p in probs1 if p > 0)
        else:
            S1_real = 0.0
        S_real_list1.append(S1_real)

        # Sunc: 非時間相関
        S1_unc = sunc_xy(x1, y1)
        S_unc_list1.append(S1_unc)

        # Srand: ランダム
        S1_rand = srand_xy(x1, y1)
        S_rand_list1.append(S1_rand)




        # --- main 側（agent） ---
        counter2 = Counter(trace_list2)  # (x1,y1,t1,x2,y2,t2)
        total2 = sum(counter2.values())
        if total2 > 0:
            probs2 = (c / total2 for c in counter2.values())
            S2_real = -sum(p * log2(p) for p in probs2 if p > 0)
        else:
            S2_real = 0.0
        S_real_list2.append(S2_real)

        S2_unc = sunc_xy(x2, y2)
        S_unc_list2.append(S2_unc)

        S2_rand = srand_xy(x2, y2)
        S_rand_list2.append(S2_rand)








    # --- ヒストグラム（カーネル密度推定も） ---
    import matplotlib.pyplot as plt

    print(S_real_list1)
    #print(S_unc_list1)
    #print(S_rand_list1)
    #print(S_real_list2)
    #print(S_unc_list2)
    #print(S_rand_list2)

    sns.set()
    sns.distplot(S_real_list1, bins=30)
    sns.distplot(S_unc_list1, bins=30)
    sns.distplot(S_rand_list1, bins=30)
    plt.legend(labels=["Sreal", "Sunc", "Srand"])
    plt.xlabel("Entropy",fontsize=14, color="black")
    plt.ylabel("P(S)",fontsize=14, color="black")
    plt.title("Entropy distribution",fontsize=20, color="black")
    plt.tight_layout()
    plt.savefig('result/_graph/time_mesh_data_yjmob_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close()



    sns.set()
    sns.distplot(S_real_list2, bins=30)
    sns.distplot(S_unc_list2, bins=30)
    sns.distplot(S_rand_list2, bins=30)
    plt.legend(labels=["Sreal", "Sunc", "Srand"])
    plt.xlabel("Entropy",fontsize=14, color="black")
    plt.ylabel("P(S)",fontsize=14, color="black")
    plt.title("Entropy distribution",fontsize=20, color="black")
    plt.tight_layout()
    plt.savefig('result/_graph/time_mesh_main_yjmob_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close()












