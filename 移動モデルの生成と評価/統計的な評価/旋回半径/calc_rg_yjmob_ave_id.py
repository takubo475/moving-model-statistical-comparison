import fractions
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
import shutil
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

effective_digits = 2

id_start = int(0)
id_end =int(401)

def impdata(fname):
    rg_list=[]
    s_list=[]
    pattern1 = r'(-?\d+.\d+)'
    pattern2 = "s"+'(-?\d+)'

    infile = open(str(fname), "r")  ##旋回半径計算/rg_yjmob/

    a=infile.readline()
    r=infile.readline()

    for line in infile:
        flug = "0"
        flug = re.search(pattern2, str(line))
        data= re.search(pattern1, str(line))
        if flug==None:
            data= re.search(pattern1, str(line))
            rg_list.append(data.group(1))

        else:
            s_list.append(data.group(1))

    infile.close()

    return rg_list, s_list






if __name__ == '__main__':
    pass

    RGX_max=-10.0
    RGX_min=-10.0
    PL_RG1=[]
    PL_RG2=[]
    PL_RG_list1=[]
    PL_RG_list2=[]
    PL_RG_ER_list=[]
    PL_S_list1=[]
    PL_S_list2=[]
    uid_list = []
    err_uid_list = []


    for uid in range(id_start,id_end):

        RG_list1=[]
        RG_list2=[]
        S_list1=[]
        S_list2=[]
        RG1=[]
        RG2=[]
        RG_list_queue = []
        S_list_queue =[]



        fname2 = 'result/rg_yjmob_uid'+str(uid)+'_data.txt'
        fname1 = 'result/rg_yjmob_uid'+str(uid)+'_irl200_ep500000.txt'

        
        try:
            RG_list_queue, S_list_queue=impdata(fname1)
            uid_list.append(uid)
        except:
            continue


        RG1.append(float(RG_list_queue[0]))
        PL_RG1.append(float(RG_list_queue[0]))
        ###誤差のリストのためのuidを記録
        err_uid_list.append(uid)
        for i in range(1,len(RG_list_queue)):
            RG_list1.append(float(RG_list_queue[i]))
            PL_RG_list1.append(float(RG_list_queue[i]))
            if RGX_max<=float(RG_list_queue[i]):
                RGX_max=float(RG_list_queue[i])

        for i in range(len(S_list_queue)):
            S_list1.append(float(S_list_queue[i]))
            PL_S_list1.append(float(S_list_queue[i]))


        try:
            RG_list_queue, S_list_queue=impdata(fname2)
        except:
            continue



        RG2.append(float(RG_list_queue[0]))
        PL_RG2.append(float(RG_list_queue[0]))
        for i in range(1,len(RG_list1)+1):
            RG_list2.append(float(RG_list_queue[i]))
            PL_RG_list2.append(float(RG_list_queue[i]))
            if (RGX_min>=float(RG_list_queue[i]))or(RGX_min==-10.0):
                RGX_min=float(RG_list_queue[i])

        for i in range(len(S_list1)):
            S_list2.append(float(S_list_queue[i]))
            PL_S_list2.append(float(S_list_queue[i]))


    for i in range (len(PL_RG_list1)):
        try:
            ER1=abs(float(PL_RG_list2[i])-float(PL_RG_list1[i]))
            PL_RG_ER_list.append(ER1)
        except:
            continue

    corrcoef_x = np.array(PL_RG_list2)
    corrcoef_y = np.array(PL_RG_list1)  


    ###相関係数計算
    correlation_matrix = np.corrcoef(corrcoef_x, corrcoef_y)
    correlation_coefficient = correlation_matrix[0, 1]
    # 結果の表示
    print("相関行列:\n", correlation_matrix)
    print("相関係数:", correlation_coefficient)



    # print(PL_RG1)
    # print(max(PL_RG1))
    # print(min(PL_RG1))
    # print(round(((RGX_min)-0.05),2))
    # print(round(((RGX_max)+0.05),2))


#旋回半径
    ##plt.xlim((float(RGX_min))-0.05, float(RGX_max)+0.05)
    ##plt.ylim((float(RGX_min))-0.05, float(RGX_max)+0.05)

    plt.xlabel("expert",fontsize=14, color="black")
    plt.ylabel("moving model",fontsize=14, color="black")
    plt.title("Displacement distribution",fontsize=20, color="black")

    plt.xticks([0.0, round((((RGX_max)+0.05)/2.0),2), round(((RGX_max)+0.05),2)])
    ##plt.xticks([(RGX_max)+0.05],[round(((RGX_max)+0.05),2)])  ##round(((RGX_min)-0.05),2), round((((RGX_max)+0.05)/2.0),2),round(((RGX_max)+0.05),2) 
    plt.yticks([0.0, round((((RGX_max)+0.05)/2.0),2), round(((RGX_max)+0.05),2)])
    plt.plot(PL_RG_list2, PL_RG_list1, label="k=2,4,6,8,10", marker=".", linestyle="", color="blue")
    plt.plot(PL_RG2, PL_RG1, label="k = ∞", marker=".", linestyle="", color="red")


    x = np.linspace((float(RGX_min))-0.05, float(RGX_max)+0.05)
    y = x
    plt.plot(x,y, label="y = x", color="black")

    plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=8)

    plt.savefig('result/_graph/RG_yjmob_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close

##S
    ##plt.xlim(0.0,1.5)
    ##plt.ylim(0.0,1.5)

    plt.plot(PL_S_list1, PL_S_list2, marker=".", linestyle="", color="red")

    x = np.linspace(0.0,1.5)
    y = x
    plt.plot(x,y, color="black")

    plt.xticks([0.0,1.0])##0.0, 0.25, 0.5, 0.75, 1.0 , 1.25
    plt.yticks([1.25])

    plt.xlabel("expert",fontsize=14, color="black")
    plt.ylabel("created",fontsize=14, color="black")
    plt.title("S",fontsize=20, color="black")
    plt.savefig('result/_graph/S_yjmob_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close




##誤差分布
    plt.hist(PL_RG_ER_list, bins=80, color="blue")
    

    plt.xlabel("distance",fontsize=14, color="black")
    plt.ylabel("frequency",fontsize=14, color="black")
    plt.title("Error Distribution",fontsize=20, color="black")
    plt.savefig('result/_graph/err_dist_yjmob_uid'+str(id_start)+'_'+str(id_end)+'_irl200.png')
    plt.clf()
    plt.close


    f = open('result/err_rg.txt', 'w')
    for i in range (len(err_uid_list)):

        f.write('\n'+"uid = "+str(err_uid_list[i]))


        f.write(",  err = "+str(PL_RG_ER_list[i]))

    f.close()

