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
  
z=[35.66, 139.97, 35.72, 140.03] #tkb
#z=[37.55, -122.57,37.85, -122.27] #taxi
delta = z[2]-z[0]
#print(delta)
#assert z[0]-z[2] == z[1]-z[3]

apart=40
#print(apart)

effective_digits = 3
trace_list = []
infile = open('rl_coordinate.txt', "r")
for line in infile:
    data_tmp_list = line.split(" ") 
    longitude = float(data_tmp_list[1])
    latitude = float(data_tmp_list[0])
    longitude = ((z[1])+((delta/apart) * ((longitude))))
    latitude = ((z[0])+((delta/apart) * ((latitude))))
    #print(latitude)
    #print(longitude)
    trace_list.append( (round(latitude, effective_digits), round(longitude, effective_digits)) )
infile.close()
#print(trace_list)

pattern1 = r'(\d+.\d+), (-?\d+.\d+)'
trace_list = re.findall(pattern1, str(trace_list))
text = str(trace_list).translate(str.maketrans({' ': None}))
text = str(text).translate(str.maketrans({"(": '\n',  ")": ' ',  "'": ' ', "[": ' ',  "]": ' '}))
text = str(text).translate(str.maketrans({' ': None}))
text = str(text).translate(str.maketrans({",": ' '}))
text = str(text).removeprefix('\n')

f = open('rl_latlon.txt', 'w')
f.write(str(text))
f.close()
