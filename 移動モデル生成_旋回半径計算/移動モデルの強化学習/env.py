from matplotlib.pyplot import stem, step
import numpy as np
import os

class Environment():

    def __init__(self,dbname):
        self.dbname=dbname
        self.state,self.actions,self.action_conv,self.maxstep,self.pos_reward=self.importdata(self.dbname)
        #print(self.state)
        pass
        

    def get_states(self):
        return self.state
    
    def get_actions(self):
        return self.actions
    
    
    #整合性を取る
    def step(self,previous_pos,action,time): #--> state = int , action = int
        reward=0
        next_state=action
        id=self.actions[previous_pos][action][0]
        reward=self.actions[previous_pos][action][3]
        step=self.actions[previous_pos][action][4]
        route=self.actions[previous_pos][action][5]
        return id,next_state , step,reward ,route
        
    
    
    def importdata(self,name):#エクセルからデータを抽出する
        import sqlite3
        pos_list=list()
        action_list=list()
        con = sqlite3.connect('main.db')
        cur = con.cursor()
    
        #startとgoalの地点を重複なしで取得
        cur.execute('select distinct startpos from '+str(self.dbname))
        for i,n in enumerate( cur.fetchall() ):
            #pos_list.append(n[0])
            pos_list.append(i)
            #print(n[0])
        cur.execute('SELECT * FROM '+str(self.dbname))
        
        action_list=list()
        action_list.append(list())

        data=cur.fetchall()
        st=data[0][1]
        for n in data:
            if st != n[1]:
                action_list.append(list())
                st=n[1]

            action_list[-1].append([n[0],n[1],n[2],n[3],n[4],n[5]])
            #print(n)

        action_conv={}
        for i,a in enumerate( action_list):
            #print(a[0][1])
            #action_conv[i]=a[0][1]
            action_conv[i]=a[0][1]

        #step数の最大値を取得
        #print("select step from" + self.dbname + " ORDER BY step DESC limit 1")
        maxstep= cur.execute("select step from " + self.dbname + " ORDER BY step DESC limit 1").fetchone()[0]
        #print(maxstep)

        #各地点の報酬を取得
        pos_reward=list()
        for n in data:
            if n[1] == n[2]:
                pos_reward.append(n[3])
                st=n[1]

            #action_list[-1].append([n[0],n[1],n[2],n[3],n[4],n[5]])
            #print(n)

        con.close()
        return pos_list,action_list,action_conv,maxstep,pos_reward



if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    env=Environment("routes_reward0")
    #pos_list,action_list,action_conv,maxstep,pos_reward=env.importdata()
    # for i in range(0,1):
    #     env.step(i,0)
    pass
    
