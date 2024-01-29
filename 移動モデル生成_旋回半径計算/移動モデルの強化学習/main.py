import random
from qtable import Qtable
from qagent import Q_agent
from sql_controller import Sql_controller
from env import Environment
from tqdm import tqdm
import math
import matplotlib.pyplot as plt
import numpy as np
import copy
# 描画領域を取得
fig, ax = plt.subplots(1, 1)






def print_data(print_list):
    for i in print_list:
        print(i,end=" : ")
    
    print()

if __name__ == '__main__':
    epoch=2000000
    
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    sql=Sql_controller()#sqlコントローラをインポート
    #sql.insert()#startpos (int), goalpos (int), reward (int) , step (int),route (list)
    envs=list()
    for h in range(24):
        envs.append(Environment("routes_reward"+str(h)))
    #actions=env.get_states()
    states=envs[0].get_actions()
    pass
    qtable=Qtable(envs[0].get_states())#複数のエージェントが共有するため重複しないようにきおつける
    agents=list()

    #maxstep=env.maxstep
    start_pos=envs[0].pos_reward
    # print(max(start_pos))
    # print(start_pos.index(max(start_pos)))
    start_pos=start_pos.index(max(start_pos))

    for i in range(20):
        agents.append(Q_agent(envs,qtable,states,start_pos,(i)/20))#,env,actions,q_table,state
    #agents.append(Q_agent(envs,qtable,states,start_pos,0.1))#,env,actions,q_table,state
    
    r=1
    agentreward=0
    step_co=0
    y=list()
    x=list()
    for i in tqdm( range(epoch)):
        
        for j,agent in enumerate( agents):
            previous_pos,action=agent.act()#act
            
            #報酬の成形
            _,next_state,step,reward ,route=agent.step(previous_pos,action) #step
            #reward=reward*( r+ math.sqrt(r**2 - (step/maxstep)**2) )
            #reward=reward*( math.sqrt(2*(step/maxstep)*r - (step/maxstep)**2) )
            reward=reward/step
            #reward=reward/( r+ math.sqrt(r**2 - (step/maxstep)**2) )
            
            #observerで学習
            agent.observe(reward,action,next_state,step)
            
            if agent==agents[0]:
                agentreward += reward
                pos=eval(route)
                sql.insert([str(pos[0]),str(pos[-1]),reward,step,route])#start,gola,cost,step,route
                if agent.time>=1440:#60*24 １時間*24
                    sql.insert([-1,-1,-1,-1,-1])
                    
                    #agent.set_state(start_pos)
                    #print(agentstep,agentreward)
                    if step_co%1 ==0 or step_co==0:
                        y.append(agentreward)
                        x.append(step_co)
                        # x軸:時刻
                    
                    agentreward=0
                    step_co+=1
            
            if agent.time>=1440:
                agent.time=0     
                    
                
    #print(x)
    ax.set_ylim((0, max(y)*1.1))
    #x = list(range(0, len(y), 1))
    line, = ax.plot(x, y, color='blue')
    # 次の描画まで0.01秒待つ
    plt.savefig("step_reward.png")









        
       
        



    


            