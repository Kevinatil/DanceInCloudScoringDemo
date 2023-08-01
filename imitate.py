import os
import cv2
from datetime import datetime

from tkinter import filedialog
import tkinter

from utils import *
from json_funcs import *
from calculate_score import *
from imitate_ui import *

def video_capture(origin_name,save_path=rootpath+'imitate_videos/',duration=5,WIDTH=1280,HEIGHT=720,FPS=24,preview=False):
    clocklist=str(datetime.now()).split(' ')[1][:-7].split(':')
    imitate_name=origin_name+'_'+clocklist[0]+'_'+clocklist[1]+'_'+clocklist[2]+'.mp4'
    FILENAME = save_path+origin_name+'/'+imitate_name

    # 必须指定CAP_DSHOW(Direct Show)参数初始化摄像头,否则无法使用更高分辨率
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # 设置摄像头设备分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    # 设置摄像头设备帧率,如不指定,默认600
    cap.set(cv2.CAP_PROP_FPS, 24)
    # 建议使用XVID编码,图像质量和文件大小比较都兼顾的方案
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(FILENAME, fourcc, FPS, (WIDTH, HEIGHT))

    start_time = datetime.now()
    while True:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            if preview: #显示预览窗口
                cv2.imshow('Preview_Window', frame)
            if (datetime.now()-start_time).seconds == duration:
                cap.release()
                break
            # 监测到ESC按键也停止
            if cv2.waitKey(3) & 0xff == 27:
                cap.release()
                break
    out.release()
    if preview:
        cv2.destroyAllWindows()

def get_video_duration(name):
    cap = cv2.VideoCapture(name)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num =cap.get(7)
        duration = frame_num/rate
        return duration

class OpenPoseVideo():
    def __init__(self):
        self.path='openpose/bin/'
    def openposedemo_video(self,input_video,output_video,face=False,hand=False): #生成识别后的视频
        cwd=os.getcwd()
        os.chdir(self.path)
        #os.chdir('D:\\openpose-1.7.0\\build\\x64\\Release')
        command='OpenPoseDemo --video '+input_video+' --write_video '+output_video
        if face:
            command+=' --face'
        if hand:
            command+=' --hand'
        os.system(command)
        os.chdir(cwd)
    def openposedemo_json(self,input_video,output_json,face=False,hand=False): #输出json
        cwd=os.getcwd()
        os.chdir(self.path)
        #os.chdir('D:\\openpose-1.7.0\\build\\x64\\Release')
        input_video+=os.listdir(input_video)[0]
        command='OpenPoseDemo --video '+input_video+' --write_json '+output_json
        if face:
            command+=' --face'
        if hand:
            command+=' --hand'
        os.system(command)
        os.chdir(cwd)

    def openposedemo_json2(self,input_video,output_json,render=True,face=False,hand=False): #输出json
        cwd=os.getcwd()
        os.chdir(self.path)
        #os.chdir('D:\\openpose-1.7.0\\build\\x64\\Release')
        command='OpenPoseDemo --video '+input_video+' --write_json '+output_json
        if not render:
            command+=' --display 0 --render_pose 0'
        if face:
            command+=' --face'
        if hand:
            command+=' --hand'
        os.system(command)
        os.chdir(cwd)

def photo_score(ns,camera=True,pose=False,del_all=True,duration=3,imitate_video_path=None):
    pose_obj=OpenPoseVideo()
    origin_video_path=rootpath+'origin_videos/'
    origin_json_path=rootpath+'origin_jsons/'+ns+'/'
    if imitate_video_path==None:
        imitate_video_path=rootpath+'imitate_videos/'+ns+'/'
        imitate_json_path=rootpath+'imitate_jsons/'+ns+'/'
    else:
        imitate_name=imitate_video_path.split('/')[-1][:-4]
        create_path(root=rootpath+'imitate_jsons/',file_name=ns,del_all=False)
        create_path(root=rootpath+'imitate_jsons/'+ns+'/',file_name=imitate_name, del_all=del_all)
        imitate_json_path=rootpath+'imitate_jsons/'+ns+'/'+imitate_name+'/'
    if camera:
        if del_all:
            del_file(imitate_video_path[:-1])
            del_file(imitate_json_path[:-1])
        print("摄像头即将开始录制")
        video_capture(origin_name=ns,duration=int(duration+0.5))
        pose=True
    if pose:
        pose_obj.openposedemo_json2(input_video=imitate_video_path,output_json=imitate_json_path,render=False)
    time.sleep(5)
    return score_print(ns,origin_json_path,imitate_json_path)

def main():
    pygame.init()

    #ScreenSize=(1200+300,800)#屏幕大小
    ScreenSize=(1200,800)#屏幕大小

    #bgColor=(255, 204, 255)#背景颜色
    #bgColor=(255, 255, 220)#背景颜色
    bgColor=(255,255,255)#背景颜色
    btColor=(215, 252, 252)

    screen = pygame.display.set_mode(ScreenSize)
    screen.fill(bgColor)
    plt.figure()

    dfcolumns=["编号","动作评分","节奏评分","右手", "左手", "右肩", "左肩", "头与躯干", "右肩与躯干", "左肩与躯干","躯干与右髋", "躯干与左髋", "右腿与髋", "左腿与髋", "右脚", "左脚", "右脚踝", "左脚踝"]

    namelist=os.listdir(rootpath+'origin_videos/')
    scorelist=os.listdir(rootpath+'scores/')

    #records=draw_bg(screen,namelist=namelist,rankboard=True)#绘制界面
    draw_bg(screen,namelist=namelist,rankboard=True)#绘制界面

    #等待鼠标操作
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y=event.pos[0],event.pos[1]
                    if 150<x<295 and 10<y<60:#点击输入视频名称
                        namelist=os.listdir(rootpath+'origin_videos/') # 刷新原始视频名称列表
                        scorelist=os.listdir(rootpath+'scores/') # 刷新原始视频分数记录文件列表
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        reset_ui(screen)
                        pygame.display.flip()

                        #输入视频名称
                        flg=1
                        while(flg):#控制输入合法
                            name=input_str(screen,1)
                            name+='.mp4'
                            if name not in namelist:
                                fontch = pygame.font.SysFont('simHei',15)
                                txt = fontch.render('输入名称非法，请重新输入', True, (255,0,0))
                                screen.blit(txt, (5,140))
                                pygame.display.flip()
                                pygame.time.delay(500)
                                pygame.draw.rect(screen, bgColor,((0,135),(290, 45)))
                                pygame.display.flip()
                            else:
                                flg=0
                        duration=get_video_duration(rootpath+'origin_videos/'+name)
                        print('视频时长',duration)
                        insert_picture(screen,name[:-4])
                        print_duration(screen,int(duration+0.5))
                        if name[:-4]+'.csv' not in scorelist:
                            print('原视频不存在分数文件')
                            scoredf=pd.DataFrame(columns=dfcolumns)
                            scored_list=[]
                        else:
                            print('原视频存在分数文件')
                            scoredf=pd.read_csv(rootpath+'scores/'+name[:-4]+'.csv',index_col=0)
                            scored_list=list(scoredf['编号'].values)
                        print(scored_list)
                        pygame.display.flip()
                    elif 370<x<505 and 10<y<60:#播放视频
                        print('播放视频'+name)
                        insert_video(rootpath+'origin_videos/'+name)
                    elif 5<x<140 and 70<y<120:#拍照
                        tptk=tkinter.Tk()
                        tptk.withdraw()
                        test_path=filedialog.askopenfilename()
                        print_posing_info(screen,0)
                        score,name_score,rhythm_score=photo_score(ns=name[:-4],camera=False,pose=True,del_all=True,duration=duration,imitate_video_path=test_path)
                        test_name=test_path.split('/')[-1][:-4]
                        if not name_in_list(test_name,scored_list):
                            print('测试视频仍未评分')
                            row=[test_name,score,rhythm_score.mean()*100]
                            for i in range(15):
                                row+=[name_score[i][1]]
                            scoredf=pd.concat([scoredf,pd.DataFrame(np.array(row).reshape(1,-1),columns=dfcolumns)],axis=0)
                            scoredf.to_csv(rootpath+'scores/'+name[:-4]+'.csv',encoding="utf_8_sig")
                        else:
                            print('该视频已进行过分数记录')
                        
                        comment=create_polar(name_score,score,rhythm_score.mean(),name[:-4],test_name)
                        print_posing_info(screen,1)
                    elif 370<x<505 and 70<y<120:#分数
                        print_score(screen,score=score,name_score=name_score,rhythm_score=rhythm_score.mean())
                        #create_polar(name_score,score,rhythm_score.mean(),name[:-4],test_name)
                        pygame.draw.rect(screen, bgColor,((10,130),(700, 660)))
                        insert_polar(screen,name[:-4]+'_'+test_name)
                        
                        fontch=pygame.font.SysFont('simHei',30)
                        txt = fontch.render("能力分布图", True, (0,0,0))
                        screen.blit(txt, (285,180))
                        print_comment(screen,comment)
                        # if score>records[name][0]:
                        #     records[name]=score

                        #     fontch = pygame.font.SysFont('simHei',20)
                        #     txt = fontch.render(name+'视频新纪录!', True, (255,0,0))
                        #     screen.blit(txt, (725,415+50))
                        #     pygame.display.flip()
                        #     pygame.time.delay(1500)
                        #     pygame.draw.rect(screen, bgColor,((725,415+50),(200, 30)))
                        #     pygame.display.flip()
                        #     print_records(screen,namelist,records)

if __name__=='__main__':
    main()