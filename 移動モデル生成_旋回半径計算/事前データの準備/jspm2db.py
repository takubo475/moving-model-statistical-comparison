import json
import sqlite3
import time
from datetime import datetime
import re


DB_FILE = "data.db"
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('create table if not exists expart ("timestampMs","year","mon","day","hour","min","sec", "latitudeE7","longitudeE7")')
#c.execute('create table table_name (timestampMs,latitudeE7,longitudeE7)')
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(os.listdir())
pass
json_open=open("a.json","r")
json_load=json.load(json_open)
for i in json_load["locations"]:
    data = list()
    a="2023-09-27T04:38:27.431Z"

    # 正規表現を使用して日時情報を抽出
    pattern = r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{3}))?Z"
    match = re.search(pattern, i["timestamp"])

    if match:
        year, month, day, hour, minute, second, millisecond = match.groups()
        if millisecond is None:
            millisecond = "000"
        extracted_data = [int(year), int(month), int(day), int(hour), int(minute), int(second), int(millisecond)]
        #print(extracted_data)
    else:
        pass
        #print("日時情報が見つかりませんでした")


    # datetime.datetime.fromisoformat(a)
    # datetime.datetime.fromisoformat(str(i["timestamp"]))
    #epoch_time = int(i["timestamp"])/1000
    # dt = time.localtime(epoch_time)
    dt=datetime(extracted_data[0],extracted_data[1],extracted_data[2],extracted_data[3],extracted_data[4],extracted_data[5],extracted_data[6])
    #print(dt.timestamp())
    data.append(int(dt.timestamp()))
    data.append(extracted_data[0])
    data.append(extracted_data[1])
    data.append(extracted_data[2])
    data.append(extracted_data[3])
    data.append(extracted_data[4])
    data.append(extracted_data[5])
    data.append(i["latitudeE7"]/10000000)
    data.append(i["longitudeE7"]/10000000)
    print(data)
    c.execute('insert into expart values (?,?,?,?,?,?,?,?,?)', data)
    #print(i["timestamp"])
    ###print("/")
    
#print(json_load)




conn.commit()
c.close()