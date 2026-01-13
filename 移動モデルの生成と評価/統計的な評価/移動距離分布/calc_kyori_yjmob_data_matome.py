import math
import numpy as np
import sys

import matplotlib.pyplot as plt

import os
import shutil
import re

import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

effective_digits = 2

id_start = int(0)
id_end= int(401)

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


f = open('result/dis_yjmob_err_list.txt', 'w')

f.write('\n')

f.close()




def import_data(l_name1,f_name1):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name1)
    cur = con.cursor()
    cur.execute('SELECT latitudeE7, longitudeE7 FROM '+str(l_name1))
    a=cur.fetchall()
    b = len(a)
    return a, b


def import_dmain_start(l_name2, f_name2):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name2)
    cur = con.cursor()
    cur.execute('SELECT startpos FROM '+str(l_name2)+' WHERE id BETWEEN 150000 and 500000')
    c=cur.fetchall()
    d = len(c)
    return c, d

def import_dmain_goal(l_name3, f_name3):#SQLからデータを抽出する
        
    import sqlite3
    con = sqlite3.connect(f_name3)
    cur = con.cursor()
    cur.execute('SELECT goalpos FROM '+str(l_name3)+' WHERE id BETWEEN 150000 and 500000')
    e=cur.fetchall()
    f = len(e)
    return e, f


if __name__ == '__main__':
    pass

    PL_dis_list1 = []
    PL_dis_list2 = []
    PL_dis_ER_list = []


    for uid in range(id_start,id_end+1):
        x1=[]
        x2=[]
        y1=[]
        y2=[]
        dis_list1 = []
        dis_list2 = []



        file_name1 = 'data/data_yjmob_B'+str(uid)+'.db'
        file_name2 = 'main/main_yjmob_uid'+str(uid)+'_irl200_ep500000.db'

        ## dataのほう,準備
        try:
            data1, dr1=import_data("expart",file_name1)
        except:
            continue
        
        for i in range (len(data1)):
        
            pattern1 = r'(-?\d+), (-?\d+)'
            d_text1=re.search(pattern1, str(data1[i]))
            x1.append(round(float(d_text1.group(1)), effective_digits))
            y1.append(round(float(d_text1.group(2)), effective_digits))



        ##  mainのほう,準備
        try:
            dmain_start, dr2=import_dmain_start("expart",file_name2)
            dmain_goal, dr3=import_dmain_goal("expart",file_name2)
        except:
            continue

        for i in range (len(dmain_start)):
            if dmain_start[i] != dmain_goal[i]:
                pattern1 = r'(-?\d+), (-?\d+)'
                d_text2=re.search(pattern1, str(dmain_start[i]))
                x2.append(((z[0])+((delta/apart) * ((round(float(d_text2.group(1)), effective_digits))))))
                y2.append(((z[1])+((delta/apart) * ((round(float(d_text2.group(2)), effective_digits))))))

        lsize = []
        lsize.append(len(x1))
        lsize.append(len(x2))

        ## dataのほう,計算
        for i in range (1,int(min(lsize))):
            distance1 = math.sqrt((float(x1[i-1])-float(x1[i]))**2+(float(y1[i-1])-float(y1[i]))**2)
            if distance1!=0.0:
                dis_list1.append(distance1)
                PL_dis_list1.append(distance1)
        disr1=len(dis_list1)

        # dis_max1=math.sqrt(2*((delta)**2))
        # dis_delta1 = dis_max1/apart

        # dc_list1 = [0]*apart

        # for i in range(len(dis_list1)):
        #     dc_list1[int(dis_list1[i]//dis_delta1)] +=1



        

        ## mainのほう,計算
        for i in range (1,disr1+1):
            distance2 = math.sqrt((float(x2[i-1])-float(x2[i]))**2+(float(y2[i-1])-float(y2[i]))**2)
            if distance2!=0.0:
                dis_list2.append(distance2)
                PL_dis_list2.append(distance2)
        disr2=len(dis_list2)

        print(disr1)
        print(disr2)


        dis_max2=math.sqrt(2*((delta)**2))
        dis_delta2 = dis_max2/apart

        dc_list2 = [0]*apart

        for i in range(len(dis_list2)):
            dc_list2[int(dis_list2[i]//dis_delta2)] +=1






        






        # ファイルに出力



        f = open('result/dis_yjmob_uid'+str(uid)+'_data.txt', 'w')
        f.write("uid:"+str(uid))
        f.write('\n'+"dcount1:"+str(dr1))
        # f.write('\n'+"dc_list1:"+str(dc_list1))
        # f.write('\n'+"dis_count1:"+str(disr1))
        # f.write('\n'+"distance1 = "+str(dis_list1))

        f.write('\n'+"dcount2:"+str(dr2))
        f.write('\n'+"dc_list2:"+str(dc_list2))
        f.write('\n'+"dis_count2:"+str(disr2))
        f.write('\n'+"distance2 = "+str(dis_list2))
        
        f.write('\n'+"dcount3:"+str(dr3))

        f.close()


        f = open('result/dis_yjmob_err_list.txt', 'a')

        f.write('\n'+"uid:"+str(uid))

        f.write(", "+"err:"+str(float(PL_dis_list1[-1])-float(PL_dis_list2[-1])))

        f.close()






    for i in range (len(PL_dis_list1)):
        ER1=float(PL_dis_list1[i])-float(PL_dis_list2[i])
        PL_dis_ER_list.append(ER1)






        
    ##グラフ作成

    plt.hist(PL_dis_list1, bins=40, color="blue", range=(0, 100))
    

    plt.xlabel("distance",fontsize=14, color="black")
    plt.ylabel("frequency",fontsize=14, color="black")
    plt.title("Displacement distribution",fontsize=20, color="black")
    plt.savefig('result/_graph/Displacement_distribution_yjmob_data_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close



    plt.hist(PL_dis_list2, bins=40, color="red", range=(0, 100))
    plt.xlabel("distance",fontsize=14, color="black")
    plt.ylabel("frequency",fontsize=14, color="black")
    plt.title("Displacement distribution",fontsize=20, color="black")
    plt.savefig('result/_graph/Displacement_distribution_yjmob_main_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close


##両対数プロット
def ccdf_from_samples(samples, bins=40, value_range=None):
    hist, edges = np.histogram(samples, bins=bins, range=value_range)
    # 右からの累積（>=x）
    ccdf = np.cumsum(hist[::-1])[::-1].astype(float)
    ccdf /= ccdf[0] if ccdf.size > 0 and ccdf[0] > 0 else 1.0  # 総数で割る

    centers = (edges[:-1] + edges[1:]) / 2.0
    mask = (centers > 0) & (ccdf > 0)
    return centers[mask], ccdf[mask]


def fit_powerlaw_on_ccdf(x, ccdf, xmin=None):
    if xmin is not None:
        m = x >= xmin
        x_fit, y_fit = np.log(x[m]), np.log(ccdf[m])
        x_plot = x[m]
    else:
        x_fit, y_fit = np.log(x), np.log(ccdf)
        x_plot = x

    a, b = np.polyfit(x_fit, y_fit, 1)
    y_hat = np.exp(b) * (x_plot ** a)
    return a, b, x_plot, y_hat


# ===== CCDF の作成 =====
# 距離の上限はこれまでのグラフと合わせて (0, 100) を使用
x1_ccdf, ccdf1 = ccdf_from_samples(PL_dis_list1, bins=40, value_range=(0, 100))
x2_ccdf, ccdf2 = ccdf_from_samples(PL_dis_list2, bins=40, value_range=(0, 100))

# ===== フィット（必要ならテール閾値を設定）=====
# 例: 下の行を None -> 10.0 に変えると x>=10 のテールに限定してフィット
FIT_XMIN = None

a1, b1, x1_for_plot, ccdf1_fit = fit_powerlaw_on_ccdf(x1_ccdf, ccdf1, xmin=FIT_XMIN)
a2, b2, x2_for_plot, ccdf2_fit = fit_powerlaw_on_ccdf(x2_ccdf, ccdf2, xmin=FIT_XMIN)

print("[expert]    slope a1 =", a1, " intercept b1 =", b1)
print("[movement]  slope a2 =", a2, " intercept b2 =", b2)

# ===== 可視化（log-log）=====
plt.figure()
plt.loglog(x1_ccdf, ccdf1, marker="o", linestyle="none", label="expert CCDF")
plt.loglog(x1_for_plot, ccdf1_fit, linestyle="-", label=f"expert fit (slope={a1:.3f})")

plt.loglog(x2_ccdf, ccdf2, marker="o", linestyle="none", label="movement CCDF")
plt.loglog(x2_for_plot, ccdf2_fit, linestyle="-", label=f"movement fit (slope={a2:.3f})")

plt.xlabel("distance", fontsize=14, color="black")
plt.ylabel("CCDF  P(X≥x)", fontsize=14, color="black")
#plt.title("Displacement CCDF (log-log) with linear fit", fontsize=20, color="black")
plt.legend(bbox_to_anchor=(1, 1), loc="upper left", borderaxespad=0, fontsize=12)
plt.tight_layout()
plt.savefig('result/_graph/CCDF_fit_yjmob_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
plt.clf()
plt.close()