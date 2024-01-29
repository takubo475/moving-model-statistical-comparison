import numpy as np
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re


effective_digits = 6

def import_data(name):#SQLからデータを抽出する
        
    import sqlite3
    pos_list=list()
    action_list=list()
    con = sqlite3.connect('data12_5.db')
    cur = con.cursor()
    cur.execute('SELECT latitudeE7, longitudeE7 FROM '+str(name))
    a=cur.fetchall()
    return a



if __name__ == '__main__':
    pass
    data=import_data("expart")
    pattern1 = r'(\d+.\d+), (-?\d+.\d+)'
    data = re.findall(pattern1, str(data))
    text = str(data).translate(str.maketrans({' ': None}))
    text = str(text).translate(str.maketrans({"(": '\n',  ")": ' ',  "'": ' ', "[": ' ',  "]": ' '}))
    text = str(text).translate(str.maketrans({' ': None}))
    text = str(text).translate(str.maketrans({",": ' '}))
    text = str(text).removeprefix('\n')

f = open('data_latlon.txt', 'w')
f.write(str(text))
f.close()
