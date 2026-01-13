import random
import numpy as np
from env import Environment
import math
class Q_agent():
    def __init__(self,envs,q_table,state,startpos,epsilon):

        self.epsilon = epsilon#探索率
        self.reward_history = []
        self.actions =None #行動の種類
        self.envs=envs

        self.q_values = q_table
        self.state=state
        self.total_reward=0
        self.previous_pos=startpos

        self.time=0
        self.hour=0
        

    
    def reset(self):
        self.env=Environment()
        self.total_reward=0
    


    def set_state(self,state):
        self.previous_pos=state
        #print(self.previous_pos)

    def observe(self,reward,action,state,step):
        pass
        #移動後で考える
        #state s'
        #action #a
        #print("s="+str(self.previous_pos)+"a="+str(action)+"s'="+str(state)+"r="+str(reward))
        #print("...........")
        #制約条件
        #休むとペナルティー
        self.hour=math.floor(self.time/60)
        if self.hour>=24:
            self.hour=self.hour%23
        
        #print(self.hour,self.time)
        #self.hour=int(self.hour)
        #print(self.hour)
        self.q_values.learn(state, self.previous_pos,action,reward,self.hour)
        self.previous_pos=state
        self.time+=step
    
    def step(self,previous_pos,action): #--> state = int , action = int
        next_state=action
        self.actions=self.envs[self.hour].actions
        id=self.actions[previous_pos][action][0]
        reward=self.actions[previous_pos][action][3]
        step=self.actions[previous_pos][action][4]
        route=self.actions[previous_pos][action][5]
        return id,next_state , step,reward ,route

    def act (self):

        #if self.epsilon >= random.random():
        if self.epsilon >random.randrange(0, 100, 1)/100:
            #探索
            action = random.randrange(0, len(self.q_values.get_qtable()[self.hour][self.previous_pos]))
        else:
            
            tables=self.q_values.get_qtable()[self.hour][self.previous_pos]
            #maxValue = np.argmax(tables)
            maxValue =np.amax(tables)
            maxIndex = []
            for i in range(len(tables)):
                if maxValue == tables[i]:
                    maxIndex.append(i)

            action=maxIndex[random.randrange(len(maxIndex))]
        
        return self.previous_pos,action
    
    def get_state(self):
        return self.state
    

