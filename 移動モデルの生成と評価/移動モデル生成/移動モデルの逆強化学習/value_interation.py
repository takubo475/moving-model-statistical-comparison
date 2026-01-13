import random

import numpy as np
from matplotlib import pyplot as plt
from numpy.lib import RankWarning

class ValueIteration:
    def __init__(self, n_states, n_actions):
        self.n_states = n_states
        self.n_actions = n_actions
        self.reward = None
        self.move_prob=0.7
        self.policy=None
    
    def set_reward(self , reward):
        self.reward=reward
    
    def set_policy(self ):
        policy = np.ones((self.n_states,self.n_actions))
        policy = policy / self.n_actions#各状態からの遷移確立を一様に分布今回は度のグリッドからでも0.25で上下左右に遷移する。network図であればここは要書き換え
        self.policy=policy
    

    def __call__(self, gamma, epslion, reward_function=None):
        probs = self.probs
        n_states = self.n_states#16
        n_actions = self.n_actions#4
        V = np.zeros(n_states)#今回は、16行1列で初期化
    
    def pro(self,gamma=0.9,threshold=0.001):
        V = np.zeros(self.n_states)#状態数で初期化

        for c in range(100):
            delta = 0
            for s in range(self.n_states):#各状態をfor文で回す
                expected_rewards = []#期待される報酬
                for a in range(self.n_actions):
                    action_prob = self.policy[s][a]#行動確立を抽出し格納
                    reward = 0
                    for p, n_s, r in self.transitions_at(s, a):#[遷移確立,遷移先,報酬]
                        if n_s is None:#遷移先がなければ
                            reward = r#rをそのまま代入
                            continue#for 文をもう１度計算
                        reward += action_prob * p * \
                                  (r + gamma * V[int(n_s)])#現在地点から起こすアクションのポリシー(0~1)*遷移確立*(遷移先の報酬[0,1,-1]*gammma*予測した報酬の遷移先の値*ゴールしているかどうか(T ot F))
                    expected_rewards.append(reward)#予測した報酬をlistに格納
                value = sum(expected_rewards)#現在の状態から各アクションを実行した場合に予測される報酬の合計を演算して格納
                delta = max(delta, abs(value - V[s]))#既存の値deltaと今回演算した値から予測される報酬の絶対値を比較し大きいほうをdeltaに代入#各状態につき1回実行される(最小値は-4周りのグリッドからそれぞれ-1をもらうから)
                #print(value)
                V[s] = value#V[s]にはdeltaと比較せず今回の値を代入する

            #print(delta)
            if delta < threshold :#or count > self._limit_count:#もしdeltaの値がthreshold(閾値)より小さくなるまたは、制限回数に到達したら
                break#処理を終了する

        return V#報酬を保存したグリッドを返す

    def reward2policy(self):
        #policyを初期化 最大エントロピー法で実装、上書きされなければ一様に割り振られる
        #itialize
        self.set_policy()

        #閾値を定義
        threshold=0.001
        gamma=0.9
        for c in range(100):
            update_stable = True
            V=self.pro(threshold=threshold,gamma=gamma)
            #行動価値関数を計算
            for s in range(self.n_states):#状態sすべてをfor文で回す
                # Get action following to the policy (choose max prob's action).
                policy_action = np.argmax(self.policy[s])#各状態sでのポリシーの最高値を取得(もっともとるべき行動)

                # Compare with other actions.
                action_rewards = np.zeros(self.n_actions)#行動aに対する報酬を記録するnparrayを作成
                for a in range(self.n_actions):#上下左右の動きをfor文で回す
                    reward = 0#今回の報酬を0で初期化
                    for p, n_s, r in self.transitions_at(s, a):#[遷移確立,遷移先,報酬,ゴールしているかどうか]
                        if n_s is None:#もし次の状態がなければ
                            reward = r#報酬をそのまま代入
                            continue#もう１度for文を実行
                        reward += p * (r + gamma * V[int(n_s)])#報酬×()
                    action_rewards[a] = reward#起こしたアクションに対する報酬を格納
                best_action = np.argmax(action_rewards)#最もよかった行動の報酬を抽出
                if policy_action != best_action:
                    update_stable = False#安定をFalseに？実質処理終了

                # Update policy (set best_action prob=1, otherwise=0 (greedy)).
                self.policy[s] = np.zeros(self.n_actions)#状態sに対するポリシーを0で初期化
                self.policy[s][best_action] = 1.0#もっともとるべき行動のポリシーを1に設定１は100%
                #print(s,best_action)

            if update_stable :
                break

        return self.policy#policyを返す
        
        
                

    def grid2oppo(self , s,a):
        if a==s+np.sqrt(self.n_states):
            return 2
        if a==s-np.sqrt(self.n_states):
            return 0
        if a== s+1:
            return 1
        if a== s-1:
            return 3
        

    def transitions_at(self, state, action):#入力値[現在の位置,起こす行動0~3]
        reward=self.reward[state]#reward = self.reward_func(state)#現在地点の報酬を取得env.reward_func
        transition = []#遷移先のリストを初期化
        transition_probs = self.transit_func(state, action)#遷移確立を計算
        for next_state in transition_probs:#現在地点から移動できる先をfor文で回す
            prob = transition_probs[next_state]#遷移先への遷移確立を取得
            reward = self.reward[int(next_state)]#遷移先の報酬を取得
            transition.append((prob, next_state, reward))#遷移先をlistに追加[遷移確立,遷移先,報酬,ゴールしているかどうか]
        for p, n_s, r in transition:#各要素を複数の値が入ったlistから抽出
            yield p, n_s, r#各状態を分割してretrun yieldが特殊 複数回に分けて　retrunが使えると考えると楽

    def transit_func(self, state, action):#変遷できるか
        transition_probs = {}#probsを保存する辞書を作成
        opposite_direction = action#アクションに応じた値を取得0であれば2(Rigth)
        candidates = [a for a in range(self.n_actions)
                      if a != opposite_direction]#アクションの候補を取得(指定されたアクションopposite_direction以外の選択)
        #opposite_directionが2であれば[0,1,3]

        for a in candidates:#アクションの候補でfor文を回す
            prob = 0#移動確立を0に設定(初期化)
            if a == action:#起こすアクションと今回の候補が一致していれば
                prob = self.move_prob#デフォルトの値を代入
            else:
                prob = (1 - self.move_prob) / 3#一致していなければ0.1 (0.2)/2


            next_state = self.move(state, a)#次の状態を決定
            #print(next_state,a)
            if next_state!=None:
                if next_state not in transition_probs:#次の状態がすでに追加されていれば
                    transition_probs[next_state] = prob#繊維確立を更新
                else:
                    transition_probs[next_state] += prob#すでに追加されていれば遷移確立を更新

        return transition_probs#遷移確立

    def move(self,s,a):
        row, col = self.state_to_coordinate(s)
        if a==0:#上
            return self.coordinate_to_state(row-1,col)
        if a==1:#右
            return self.coordinate_to_state(row,col+1)
        if a==2:#下
            return self.coordinate_to_state(row+1,col)
        if a==3:#左
            return self.coordinate_to_state(row,col-1)

    def chack_access(self,state,action,reward):
        s_action=list()
        row, col = self.state_to_coordinate(state)
        #print(row,col)
        #グリッドのみ対応
        s_action.append(self.coordinate_to_state(row-1,col))
        s_action.append(self.coordinate_to_state(row+1,col))
        s_action.append(self.coordinate_to_state(row,col-1))
        s_action.append(self.coordinate_to_state(row,col+1))
                
        return s_action


    def get_reward(self , action,reward):
        #print(action)
        s_reward=list()
        for ac in action:
            if ac==None:
                pass
                s_reward.append(None)
            else:
                #print(ac , end=",")
                #print(reward[int(ac)-1])
                s_reward.append(reward[int(ac)-1])
                pass
        
        return s_reward
        
    def state_to_coordinate(self, s):#状態を入力し座標を演算
        row, col = divmod(s, np.sqrt(self.n_states))
        return row, col
    
    def coordinate_to_state(self, row, col):
        index = row * np.sqrt(self.n_states) + col
        if index<=-1:
            return None
        
        if index>=self.n_states:
            return None
        return index
    



