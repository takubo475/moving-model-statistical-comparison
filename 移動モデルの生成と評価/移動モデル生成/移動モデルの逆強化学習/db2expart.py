import numpy as np
import sqlite3
# from gym.envs.toy_text import discrete
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def db2trajectory(hour):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM expart WHERE "hour" == '+ str(hour))
    #cur.execute('SELECT * FROM expart')
    #
    #z1---------z2
    #|           |
    #|           |
    #|           |
    #|           |
    #z3---------z4
    #delta=0.06
    
    z=[1.00, 1.00,200.00, 200.00]
    delta=z[2]-z[0]


    
    print((z[2]-z[0]),(z[3]-z[1]))
    #assert z[0]-z[2] == z[1]-z[3]
    #print(z[0]-z[2] , z[1]-z[3])
    xapart=[]
    yapart=[]

    apart=40
    grid=np.zeros([apart,apart])
    
    for i in range(apart):
        xapart.append(round(z[0]+delta/apart*i, 4))
        yapart.append(round(z[1]+delta/apart*i, 4))
    
    first=cur.fetchone()
    now=[first[1],first[2],first[3]]
    trajectory=[]
    trajectory.append([])

    for row in cur:
        if now[0]!=row[1] or now[1]!=row[2] or now[2]!=row[3]:
            if len(trajectory[-1])!=0:
                trajectory.append([])
            now=[row[1],row[2],row[3]]
        #print(row[7],row[8])
        x=y=int()
        if row[7]<=z[2] and z[0]<=row[7] and  row[8]<=z[3] and z[1]<=row[8]:
            for x in range(apart):
                if row[7]<=xapart[x]:
                    break

            for y in range(apart):
                if row[8]<=yapart[y] :
                    break
            
            #print(x,y,xapart[x],yapart[y])
            
            if grid[apart-x][y]<=1000:
                grid[apart-x][y]+=1
                trajectory[-1].append(apart*apart-(x * apart - y))

    if len(trajectory[-1])==0:
        del trajectory[-1]

    
    con.close()
    return trajectory,apart*apart
    
#db2trajectory()