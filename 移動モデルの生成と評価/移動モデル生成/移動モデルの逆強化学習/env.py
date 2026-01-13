class env():
    def __init__(self,grid,moveprob=0.9):
        self.grid = grid
        self._actions = {
            "LEFT": 0,
            "DOWN": 1,
            "RIGHT": 2,
            "UP": 3,
        }#アクションに対する値を定義
        self.move_prob = moveprob#行動確立
    
    
