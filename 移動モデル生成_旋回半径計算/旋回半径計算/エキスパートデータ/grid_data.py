import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re

#
#z1---------z2
#|           |
#|           |
#|           |
#|           |
#z3---------z4
  
z=[35.66, 139.97, 35.72, 140.03]
#z=[37.55, -122.57,37.85, -122.27]
delta = z[2]-z[0]
#print(delta)
#assert z[0]-z[2] == z[1]-z[3]
xapart=[]
yapart=[]

apart=40
grid=np.zeros([apart,apart])
#print(apart)

effective_digits = 6
trajectory=[]
latitude_list=[]
longitude_list=[]

for i in range(apart):
        xapart.append(round(z[0]+delta/apart*i, 4))
        yapart.append(round(z[1]+delta/apart*i, 4))
        #print(xapart[i],yapart[i])

infile = open('data_latlon.txt', "r")
for line in infile:
    data_tmp_list = line.split(" ") 
    longitude = float(data_tmp_list[1])
    latitude = float(data_tmp_list[0])
    latitude_list.append(latitude)
    longitude_list.append(longitude)


#print(longitude_list)    

for j in range(len(latitude_list)):
    x=y=int()
    #print(latitude_list[j])
    if (latitude_list[j]<=z[2]) and (z[0]<=latitude_list[j]) and  (longitude_list[j]<=z[3]) and (z[1]<=longitude_list[j]):
        #print(1)
        for x in range(apart):
            #print(x)
            if latitude_list[j]<=xapart[x]:
                break

        for y in range(apart):
            if longitude_list[j]<=yapart[y] :
                break

        #print(x,y)
            
        if grid[apart-x][y]<=1000:
            grid[apart-x][y]+=1 
            trajectory.append((round(latitude_list[j], effective_digits), round(longitude_list[j], effective_digits)))

#print(trajectory)            

pattern1 = r'(\d+.\d+), (-?\d+.\d+)'
trace_list = re.findall(pattern1, str(trajectory))
text = str(trace_list).translate(str.maketrans({' ': None}))
text = str(text).translate(str.maketrans({"(": '\n',  ")": ' ',  "'": ' ', "[": ' ',  "]": ' '}))
text = str(text).translate(str.maketrans({' ': None}))
text = str(text).translate(str.maketrans({",": ' '}))
text = str(text).removeprefix('\n')

f = open('data_latlon.txt', 'w')
f.write(str(text))
f.close()












