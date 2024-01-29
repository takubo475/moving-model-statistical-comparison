import numpy as np
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import re


def import_data_start(name):#SQLからデータを抽出する
        
    import sqlite3
    pos_list=list()
    action_list=list()
    con = sqlite3.connect('main_ex_200_2000000.db')
    cur = con.cursor()
    cur.execute('SELECT startpos FROM '+str(name)+' WHERE id BETWEEN 0 and 150000')
    a=cur.fetchall()
    return a

def import_data_goal(name):#SQLからデータを抽出する
        
    import sqlite3
    pos_list=list()
    action_list=list()
    con = sqlite3.connect('main_ex_200_2000000.db')
    cur = con.cursor()
    cur.execute('SELECT goalpos FROM '+str(name)+' WHERE id BETWEEN 0 and 150000')
    b=cur.fetchall()
    return b


if __name__ == '__main__':
    pass
    data=[]
    data_start=import_data_start("expart")
    data_goal=import_data_goal("expart")
    for i in range (len(data_start)):
        if data_start[i] != data_goal[i]:
            data.append(data_start[i])
    pattern1 = r'(\d+), (-?\d+)'
    data = re.findall(pattern1, str(data))
    text = str(data).translate(str.maketrans({' ': None}))
    text = str(text).translate(str.maketrans({"(": '\n',  ")": ' ',  "'": ' ', "[": ' ',  "]": ' '}))
    text = str(text).translate(str.maketrans({' ': None}))
    text = str(text).translate(str.maketrans({",": ' '}))
    text = str(text).removeprefix('\n')
    #print(str(text))

    f = open('rl_coordinate.txt', 'w')
    f.write(str(text))
    f.close()
