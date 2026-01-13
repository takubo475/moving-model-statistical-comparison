import json
import sqlite3
import time
import re
import datetime

num=32

DB_FILE = "data_yjmob_B"+str(num)+".db"
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('create table if not exists expart ("timestampMs","year","mon","day","hour","min","sec", "latitudeE7","longitudeE7")')

data_list = []
test=[]
check1=0
check2=0

infile = open('yjmob100k-dataset2.csv', "r")
line_counter = 0 # データ読み込み行の初期化

for line in infile:
    if line_counter == 0:
      line_counter += 1 # 読み込んだデータの行数を更新
    elif line_counter != 0:
      # splitで空白文字" "を区切り文字にして数値列を分割
      d1_list = line.replace("\n", "").split(",")
      test.append(d1_list)

      if d1_list[0]==f'{str(num)}':  #idを絞って一人分のデータにする

        check1=1
        data=list()
        sec=int(0)
        min=int((int(d1_list[2]) % 2)*30)
        hour=int(int(d1_list[2])//2)
        day=int(int(d1_list[1]) % 30)
        mon=int(0 + int(d1_list[1])//30)
        year=int(0 + int(d1_list[1])//360)
        x=int(d1_list[3])
        y=int(d1_list[4])

        data.append(int(0))
        data.append(year)
        data.append(mon)
        data.append(day)
        data.append(hour)
        data.append(min)
        data.append(sec)
        data.append(x)
        data.append(y)
        data_list.append(data)
        # print(data)

      elif (d1_list[0] != '0') and (check1 == 1):
        break
         

# data_list.reverse()
for i in range(len(data_list)):
    c.execute('insert into expart values (?,?,?,?,?,?,?,?,?)', data_list[i])


conn.commit()
c.close()

# f = open('test.txt', 'w')
# f.write(str(test))
# f.close()