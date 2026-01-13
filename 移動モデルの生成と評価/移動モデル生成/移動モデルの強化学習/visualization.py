import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import copy

from PIL import ImageFont
from PIL import ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ac=40

class Vis():

    def __init__(self):
        path = './result'
        try:
            os.mkdir(path)
        except:
            pass
        
        fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')  # コーデックの指定
        self.video  = cv2.VideoWriter('./result/movie.mp4', fourcc, 60.0, (640, 480))  # VideoWriter型のオブジェクトを生成、再生速度60fps、サイズは画像と同じにする
        
        

        from PIL import Image
        self.img=list()
        for h in range(24):
            self.img.append(Image.open("./materials/IRL_reward"+str(h)+".png").convert("RGBA"))
        self.startmark = Image.open("./materials/start.png").convert("RGBA")
        self.goalmark = Image.open("./materials/goal.png").convert("RGBA")
        self.agentmark = Image.open("./materials/agent.png").convert("RGBA")

        # 必要であれば、ウォーターマークをリサイズする
        self.startmark.thumbnail((10, 10))
        self.goalmark.thumbnail((10, 10))
        self.agentmark.thumbnail((10, 10))

        # ウォーターマークを貼り付ける
        x_off=70
        y_off=49
        self.x_list=list()
        self.y_list=list()

        for i in range(1,ac+1):
            if i%10 :
                self.x_list.append(x_off+i*10)
            else:
                self.x_list.append(x_off+i*10)
                x_off-=1

        for i in range(1,ac+1):
            if i%5 :
                self.y_list.append(y_off+i*9)
            else:
                self.y_list.append(y_off+i*9)
                y_off+=1

    def synthetic(self,route,time):

        start,goal = route[0],route[-1]
        #print(int(time/60)%24)
        img=copy.deepcopy( self.img[int(time/60)%24])
        img.paste(self.startmark, (self.x_list[start[1]] ,self.y_list[ac-1-start[0]]), self.startmark)
        img.paste(self.goalmark, (self.x_list[goal[1]] ,self.y_list[ac-1-goal[0]]), self.goalmark)
       

        
        for r in route:
            back=copy.deepcopy(img)

            back.paste(self.agentmark, (self.x_list[r[1]] ,self.y_list[ac-1-r[0]]), self.agentmark)

            back=self.pil2cv(back)
            cv2.putText(back,
                        text=str(int(time/60))+":"+str(int(time%60)),
                        org=(200, 50),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1.0,
                        color=(0, 255, 0),
                        thickness=2,
                        lineType=cv2.LINE_4)
            
            cv2.imwrite("./result/0.png", back)
            self.video.write(cv2.imread("./result/0.png"))  # 動画の生成
            time+=1
            
        return time



    def dest(self):
        self.video.release()  # 動画ファイルを閉じる
        os.remove("./result/0.png")
    
    def pil2cv(self,image):
        ''' PIL型 -> OpenCV型 '''
        new_image = np.array(image, dtype=np.uint8)
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        return new_image

def import_reward():#エクセルからデータを抽出する
    
    array=np.zeros((ac,ac))
    import openpyxl
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    for h in range(24):
        wb = openpyxl.load_workbook("./input_data/ex100/result"+str(h)+".xlsx")
        ws = wb.worksheets[0]
        x=0
        y=0

        for i in range(ac):
            for j in range(ac):
                a=ws.cell(1+(i*ac)+j, 2)
                array[i][j]=a.value
        plt.close()
        
        
        plt.figure()
        fig, ax = plt.subplots()
        plt.pcolor(array[::-1, :])
        plt.colorbar()
        
        plt.title("", fontname="MS Gothic")
        plt.savefig('./materials/IRL_reward'+str(h)+'.png')
        plt.close()

def import_data(name):#SQLからデータを抽出する
        
    import sqlite3
    pos_list=list()
    action_list=list()
    con = sqlite3.connect('main.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM '+str(name) +' ORDER BY id DESC LIMIT 5000')
    #cur.execute('SELECT * FROM '+str(name) )
    
    a=cur.fetchall()
    a.reverse()
    return a


if __name__ == '__main__':
    pass
    
    import_reward()
    vis=Vis()
    data=import_data("expart")
    #fig = plt.figure()
    time=0 #0~1440
    flag=False
    from tqdm import tqdm
    for d in tqdm(range(len(data))) :
        if data[d][-1]==-1:
            pass
            time=0
            flag=True
        elif flag==True :
            route=eval(data[d][-1])
            #print(a)
            start,goal = route[0],route[-1]
            time=vis.synthetic(route,time)

    vis.dest()