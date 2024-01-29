import numpy as np
class Qtable():
    def __init__(self,_state):
        self.alpha = 0.2
        self.gamma = 0.99
        self.state=_state
        #Qtableを作成
        self.q_values = {}
        for h in range(24):
            self.q_values[h]=dict()
            for state in self.state:
                self.q_values[h][state] = np.repeat(0.0, len(self.state))
        
        pass

    def get_qtable(self):
        return self.q_values
    
    def qtable_setup(self,env):#滞在報酬をすべての状態で学習する
        
        print(env.get_states())
        for s in env.get_states():
            id,next_state,step,reward ,route=env.step(s,s) #step
            self.learn(next_state,next_state,s,reward)
        pass

    def learn(self, state,previous_pos,action,reward,time):
        #Qテーブルを更新
        q = self.q_values[time][previous_pos][action]  # Q(s, a)
        max_q = max(self.q_values[time][state])  # max Q(s')
        # Q(s, a) = Q(s, a) + alpha*(r+gamma*maxQ(s')-Q(s, a))
        self.q_values[time][previous_pos][action] = q + (self.alpha * (reward + (self.gamma * max_q) - q))

