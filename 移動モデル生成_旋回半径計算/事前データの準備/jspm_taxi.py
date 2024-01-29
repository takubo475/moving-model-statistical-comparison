import json
import sqlite3
import time
import re
import datetime

DB_FILE = "data.db"
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('create table if not exists expart ("timestampMs","year","mon","day","hour","min","sec", "latitudeE7","longitudeE7")')

data_list = []

infile = open('new_equioc.txt', "r")
for line in infile:
    data_tmp_list = line.split(" ") 
    unixtime = int(data_tmp_list[3].replace('\r\n',''))
    dt = datetime.datetime.fromtimestamp(unixtime)
    longitude = float(data_tmp_list[1])
    latitude = float(data_tmp_list[0])
    data = list()

    pattern = r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})"
    match = re.search(pattern,str(dt))

    if match:
        year, month, day, hour, minute, second = match.groups()
        extracted_data = [int(year), int(month), int(day), int(hour), int(minute), int(second)]
        #print(extracted_data)
    else:
        pass


    data.append(int(dt.timestamp()))
    data.append(extracted_data[0])
    data.append(extracted_data[1])
    data.append(extracted_data[2])
    data.append(extracted_data[3])
    data.append(extracted_data[4])
    data.append(extracted_data[5])
    data.append(latitude)
    data.append(longitude)
    data_list.append(data)

data_list.reverse()
for i in range(len(data_list)):
    c.execute('insert into expart values (?,?,?,?,?,?,?,?,?)', data_list[i])


conn.commit()
c.close()