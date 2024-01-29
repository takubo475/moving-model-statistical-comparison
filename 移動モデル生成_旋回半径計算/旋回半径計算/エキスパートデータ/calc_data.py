import fractions
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
import shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))


effective_digits = 2

#
#z1---------z2
#|           |
#|           |
#|           |
#|           |
#z3---------z4
  
z=[35.66, 139.97,35.72, 140.03] #tkb
#z=[37.55, -122.57,37.85, -122.27] #taxi
delta = z[2]-z[0]
#print(delta)
#assert z[0]-z[2] == z[1]-z[3]

# 格納
# ビットマップ外のデータを除く
trace_list = []
infile = open('data_latlon.txt', "r")
for line in infile:
    data_tmp_list = line.split(" ") 
    longitude = float(data_tmp_list[1])
    latitude = float(data_tmp_list[0])
    counter =0

    if (latitude >= z[2]) or (latitude <= z[0]):
        counter+=1
  
    if (longitude >= z[3]) or (longitude <= z[1]):
        counter+=1
   
    if counter == 0:
        trace_list.append( (round(latitude, effective_digits), round(longitude, effective_digits)) )

infile.close()

# 重心計算
cm_lat = 0
cm_lon = 0
r_cm = []
for i in range (len(trace_list)):
  cm_lat += trace_list[i][0]
  cm_lon += trace_list[i][1]
cm_lat = cm_lat / float(len(trace_list))
cm_lon = cm_lon / float(len(trace_list))
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

#S2
s2 = 0
s2 = (R_g2)/(R_g)
#print(s2)


# k(=4)-旋回半径(移動半径) r_g^{(k)} の計算
#R_g4
R_g4_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0]) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1])
R_g4_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1]) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1])

# r_g^{(4)}
R_g4 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g4_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g4_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g4_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g4_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g4_cm_lon)**2 ))
R_g4 = np.sqrt(R_g4/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1]))

#s4
s4 = (R_g4)/(R_g)


# k(=6)-旋回半径(移動半径) r_g^{(k)} の計算
#R_g6
R_g6_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][0] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][0] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1])
R_g6_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][1] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][1] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1])

# r_g^{(6)}
R_g6 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[4][1] * ( (sorted_frequency_dict[4][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[4][0][1] - R_g6_cm_lon)**2 )) + (sorted_frequency_dict[5][1] * ( (sorted_frequency_dict[5][0][0] - R_g6_cm_lat)**2 + (sorted_frequency_dict[5][0][1] - R_g6_cm_lon)**2 ))
R_g6 = np.sqrt(R_g6/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1]))

#s6
s6 = (R_g6)/(R_g)

# k(=8)-旋回半径(移動半径) r_g^{(k)} の計算
#R_g8
R_g8_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][0] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][0] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][0] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][0] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1])
R_g8_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][1] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][1] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][1] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][1] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1])

# r_g^{(8)}
R_g8 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[4][1] * ( (sorted_frequency_dict[4][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[4][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[5][1] * ( (sorted_frequency_dict[5][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[5][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[6][1] * ( (sorted_frequency_dict[6][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[6][0][1] - R_g8_cm_lon)**2 )) + (sorted_frequency_dict[7][1] * ( (sorted_frequency_dict[7][0][0] - R_g8_cm_lat)**2 + (sorted_frequency_dict[7][0][1] - R_g8_cm_lon)**2 ))
R_g8 = np.sqrt(R_g8/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1]))

#s8
s8 = (R_g8)/(R_g)

# k(=10)-旋回半径(移動半径) r_g^{(k)} の計算
#R_g10
R_g10_cm_lat = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][0] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][0] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][0] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][0] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][0] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][0] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][0] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][0] + sorted_frequency_dict[8][1] * sorted_frequency_dict[8][0][0] + sorted_frequency_dict[9][1] * sorted_frequency_dict[9][0][0] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1] + sorted_frequency_dict[8][1] + sorted_frequency_dict[9][1])
R_g10_cm_lon = (sorted_frequency_dict[0][1] * sorted_frequency_dict[0][0][1] + sorted_frequency_dict[1][1] * sorted_frequency_dict[1][0][1] + sorted_frequency_dict[2][1] * sorted_frequency_dict[2][0][1] + sorted_frequency_dict[3][1] * sorted_frequency_dict[3][0][1] + sorted_frequency_dict[4][1] * sorted_frequency_dict[4][0][1] + sorted_frequency_dict[5][1] * sorted_frequency_dict[5][0][1] + sorted_frequency_dict[6][1] * sorted_frequency_dict[6][0][1] + sorted_frequency_dict[7][1] * sorted_frequency_dict[7][0][1] + sorted_frequency_dict[8][1] * sorted_frequency_dict[8][0][1] + sorted_frequency_dict[9][1] * sorted_frequency_dict[9][0][1] ) /(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1] + sorted_frequency_dict[8][1] + sorted_frequency_dict[9][1])

# r_g^{(10)}
R_g10 = (sorted_frequency_dict[0][1] * ( (sorted_frequency_dict[0][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[0][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[1][1] * ( (sorted_frequency_dict[1][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[1][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[2][1] * ( (sorted_frequency_dict[2][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[2][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[3][1] * ( (sorted_frequency_dict[3][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[3][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[4][1] * ( (sorted_frequency_dict[4][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[4][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[5][1] * ( (sorted_frequency_dict[5][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[5][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[6][1] * ( (sorted_frequency_dict[6][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[6][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[7][1] * ( (sorted_frequency_dict[7][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[7][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[8][1] * ( (sorted_frequency_dict[8][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[8][0][1] - R_g10_cm_lon)**2 )) + (sorted_frequency_dict[9][1] * ( (sorted_frequency_dict[9][0][0] - R_g10_cm_lat)**2 + (sorted_frequency_dict[9][0][1] - R_g10_cm_lon)**2 ))
R_g10 = np.sqrt(R_g10/float(sorted_frequency_dict[0][1] + sorted_frequency_dict[1][1] + sorted_frequency_dict[2][1] + sorted_frequency_dict[3][1] + sorted_frequency_dict[4][1] + sorted_frequency_dict[5][1] + sorted_frequency_dict[6][1] + sorted_frequency_dict[7][1] + sorted_frequency_dict[8][1] + sorted_frequency_dict[9][1]))

# #s10
s10 = (R_g10)/(R_g)

# ファイルに出力
f = open('data_rg_expart.txt', 'w')
f.write("R_cm = "+str(r_cm))
f.write('\n'+"R_g = "+str(R_g))
f.write('\n'+"R_g2 = "+str(R_g2))
f.write('\n'+"s2 = "+str(s2))
f.write('\n'+"R_g4 = "+str(R_g4))
f.write('\n'+"s4 = "+str(s4))
f.write('\n'+"R_g6 = "+str(R_g6))
f.write('\n'+"s6 = "+str(s6))
f.write('\n'+"R_g8 = "+str(R_g8))
f.write('\n'+"s8 = "+str(s8))
f.write('\n'+"R_g10 = "+str(R_g10))
f.write('\n'+"s10 = "+str(s10))
f.close()

f = open('data_frequency_expart.txt', 'w')
f.write("エキスパートの訪問頻度1番目から10番目:")
f.write('\n'+"1番目:"+str(sorted_frequency_dict[0]))
f.write('\n'+"2番目:"+str(sorted_frequency_dict[1]))
f.write('\n'+"3番目:"+str(sorted_frequency_dict[2]))
f.write('\n'+"4番目:"+str(sorted_frequency_dict[3]))
f.write('\n'+"5番目:"+str(sorted_frequency_dict[4]))
f.write('\n'+"6番目:"+str(sorted_frequency_dict[5]))
f.write('\n'+"7番目:"+str(sorted_frequency_dict[6]))
f.write('\n'+"8番目:"+str(sorted_frequency_dict[7]))
f.write('\n'+"9番目:"+str(sorted_frequency_dict[8]))
f.write('\n'+"10番目:"+str(sorted_frequency_dict[9]))
f.close()

print(len(trace_list))

