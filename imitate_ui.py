import pygame
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from pygame.locals import *

#bgColor=(255, 204, 255)#背景颜色
#bgColor=(255, 255, 220)#背景颜色
bgColor=(255,255,255)#背景颜色
btColor=(215, 252, 252)#按钮颜色

rootpath='activity/score_video_ui2/'

def draw_bg(screen,namelist,rankboard=True):#绘制背景
    pygame.display.set_caption("Imitate Show")#标题

    pygame.draw.aaline(screen,(0,0,0),(720,0),(720,800))#绘制分割线
    pygame.draw.aaline(screen,(0,0,0),(960,0),(960,400))#绘制分割线
    pygame.draw.line(screen,(0,0,0),(1200,0),(1200,800),width=3)#绘制分割线
    d=50
    for i in range(1,10):
        pygame.draw.aaline(screen,(0,0,0),(720,i*d),(1200,i*d))#绘制分割线

    #提示信息
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("输入视频名称", True, (0,0,0))
    screen.blit(txt, (5,22))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("最高纪录", True, (0,0,0))
    screen.blit(txt, (1302,14))
    #设置按钮
    pygame.draw.rect(screen, btColor,((150,10),(145, 50)))

    pygame.draw.rect(screen, btColor,((370,10),(135, 50)))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("原始视频", True, (0,0,0))
    screen.blit(txt, (393,24))

    pygame.draw.rect(screen, btColor,((5,70),(135, 50)))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("选择视频", True, (0,0,0))
    screen.blit(txt, (28,84))

    pygame.draw.rect(screen, btColor,((370,70),(135, 50)))
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render("查看分数", True, (0,0,0))
    screen.blit(txt, (393,84))

    # if rankboard:
    #     b=300
    #     n=len(namelist)
    #     records=pd.read_csv(rootpath+'/records.csv',index_col=0,header=0)
    #     print(records)
    #     pygame.draw.aaline(screen,(0,0,0),(1200,50),(1200+b,50))#绘制分割线
    #     pygame.draw.aaline(screen,(0,0,0),(1200+b//2,50),(1200+b//2,50+50*n))#绘制分割线
    #     fontch = pygame.font.SysFont('simHei',20)
    #     for i in range(2,n+2):
    #         pygame.draw.aaline(screen,(0,0,0),(1200,50*i),(1200+b,50*i))#绘制分割线
    #         txt = fontch.render(namelist[i-2], True, (0,0,0))
    #         l=len(namelist[i-2])
    #         screen.blit(txt, (1200+(150-l*10)//2,50*i-35))
    #         s='{0:.2f}'.format(records[namelist[i-2]][0])
    #         txt = fontch.render(s, True, (0,0,0))
    #         l=len(s)
    #         screen.blit(txt, (1350+(150-l*10)//2,50*i-35))

        # logo
        # path=rootpath+'/scorepic/'+'logo.png'
        # pic = pygame.image.load(path).convert()
        # pic = pygame.transform.scale(pic, (200,200))
        # screen.blit(pic, (1250,575))
    
    pygame.display.flip()

    #return records


def print_score(screen,score,name_score,rhythm_score):#打印
    # if rhythm_score>=0:
    #     name_score.append(['节奏',rhythm_score*100])
    fontch = pygame.font.SysFont('simHei',20)
    for i in range(len(name_score)):
        r=i//2
        c=i%2
        #tp=name_score[i][0]+':  '+str(int(name_score[i][1]*100)/100)
        tp='{0}:{1}{2:.2f}'.format(name_score[i][0],' '*(12-len(name_score[i][0])*2),name_score[i][1])
        txt = fontch.render(tp, True, (0,0,0))
        screen.blit(txt, (730+c*240,15+r*50))
    txt = fontch.render('动作得分:  {0:.2f}'.format(score), True, (0,0,0))
    screen.blit(txt, (730,415))
    if rhythm_score>=0:
        if score<80:
            txt = fontch.render('(节奏得分:  无效)', True, (0,0,0))
        else:
            txt = fontch.render('(节奏得分:  {0:.2f})'.format(rhythm_score*100), True, (0,0,0))
        screen.blit(txt, (970,415))
    print('节奏分',rhythm_score.mean())

    fontch = pygame.font.SysFont('simHei',30)
    txt=fontch.render('动作评级', True, (0,0,0))
    screen.blit(txt, (730,625))
    grade=0
    if score>98:
        grade=4
    elif score>95:
        grade=2
    elif score>90:
        grade=3
    elif score>80:
        grade=1
    elif score>70:
        grade=5
    elif score>60:
        grade=6
    else:
        grade=7
    #grade=1
    insert_score(screen,str(grade))
    pygame.display.flip()

def print_duration(screen,dur):
    durs='视频时长 {0} 秒'.format(dur)
    fontch = pygame.font.SysFont('simHei',22)
    txt = fontch.render(durs, True, (255,0,0))
    screen.blit(txt, (510,24))

def insert_picture(screen,name,horizontal=700,vertical=660):#插入图片
    path=rootpath+'/origin_pics/'+name+'.jpg'
    piclist=os.listdir(rootpath+'/origin_pics/')
    if not name+'.jpg' in piclist:
        return
    pic = pygame.image.load(path).convert()
    size=pic.get_size()
    
    delta1=vertical-(horizontal/size[0])*size[1] #按横向放大
    delta2=horizontal-(vertical/size[1])*size[0] #按纵向放大
    if delta1<0:
        sizek=vertical/size[1]
    elif delta2<0:
        sizek=horizontal/size[0]
    elif delta1<delta2:
        sizek=horizontal/size[0]
    else:
        sizek=vertical/size[1]
    sizeh=int(size[0]*sizek)
    sizev=int(size[1]*sizek)
    x=int((horizontal-sizeh)/2)+10
    y=int((vertical-sizev)/2)+130
    pic = pygame.transform.scale(pic, (sizeh,sizev))
    screen.blit(pic, (x,y))
    pygame.display.flip()

def insert_polar(screen,name,horizontal=700,vertical=660):#插入图片
    path=rootpath+'scores/'+name+'.png'
    print(path)
    pic = pygame.image.load(path).convert()
    size=pic.get_size()
    
    delta1=vertical-(horizontal/size[0])*size[1] #按横向放大
    delta2=horizontal-(vertical/size[1])*size[0] #按纵向放大
    if delta1<0:
        sizek=vertical/size[1]
    elif delta2<0:
        sizek=horizontal/size[0]
    elif delta1<delta2:
        sizek=horizontal/size[0]
    else:
        sizek=vertical/size[1]
    sizeh=int(size[0]*sizek)
    sizev=int(size[1]*sizek)
    x=int((horizontal-sizeh)/2)+10
    y=int((vertical-sizev)/2)+130
    pic = pygame.transform.scale(pic, (sizeh,sizev))
    screen.blit(pic, (x,y))
    pygame.display.flip()

def insert_score(screen,name,horizontal=300,vertical=300):#插入图片
    path=rootpath+'\\scorepic\\'+name+'.png'
    pic = pygame.image.load(path).convert()
    size=pic.get_size()
    
    delta1=vertical-(horizontal/size[0])*size[1] #按横向放大
    delta2=horizontal-(vertical/size[1])*size[0] #按纵向放大
    if delta1<0:
        sizek=vertical/size[1]
    elif delta2<0:
        sizek=horizontal/size[0]
    elif delta1<delta2:
        sizek=horizontal/size[0]
    else:
        sizek=vertical/size[1]
    sizeh=int(size[0]*sizek)
    sizev=int(size[1]*sizek)
    x=int((horizontal-sizeh)/2)+875
    y=int((vertical-sizev)/2)+475
    pic = pygame.transform.scale(pic, (sizeh,sizev))
    screen.blit(pic, (x,y))
    pygame.display.flip()

def insert_video(name): #插入视频
    video = cv2.VideoCapture(name)

    # 获得码率及尺寸
    fps = video.get(cv2.CAP_PROP_FPS)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # 读帧
    success, frame = video.read()
    while success:
        #frame = cv2.resize(frame, (960, 540)) # 根据视频帧大小进行缩放
        cv2.imshow('Video Preview', frame)  # 显示
        cv2.waitKey(int(1000 / int(fps)))  # 设置延迟时间
        success, frame = video.read()  # 获取下一帧
    video.release()
    cv2.destroyAllWindows()

def reset_ui(screen):
    
    pygame.draw.rect(screen, bgColor,((10,130),(700, 660)))
    pygame.draw.rect(screen, bgColor,((720,0),(480, 800)))
    pygame.draw.rect(screen, bgColor,((510,10),(180, 50)))
    pygame.draw.rect(screen, bgColor,((150,70),(140, 50)))
    pygame.draw.aaline(screen,(0,0,0),(720,0),(720,800))#绘制分割线
    pygame.draw.aaline(screen,(0,0,0),(960,0),(960,400))#绘制分割线
    d=50
    for i in range(1,10):
        pygame.draw.aaline(screen,(0,0,0),(720,i*d),(1200,i*d))#绘制分割线
    pygame.display.flip()

def input_str(screen,mode=0):#输入
    namestr=''
    flag=1
    while flag:
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key == K_BACKSPACE:#退格
                    if len(namestr)<=1:
                        namestr=''
                    else:
                        namestr = namestr[:-1]
                    #更新界面打印
                    if mode==1:#人数
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (155,25))
                        pygame.display.flip()
                    elif mode==2:#起始编号
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (520,252))
                        pygame.display.flip()
                elif event.key==K_RETURN:#回车
                    flag=0
                    if mode==1:
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        pygame.display.flip()
                    elif mode==2:
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        pygame.display.flip()
                    break
                else:#输入
                    namestr+=event.unicode
                    if mode==1:#人数
                        pygame.draw.rect(screen, btColor,((150,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (155,25))
                        pygame.display.flip()
                    elif mode==2:#起始编号
                        pygame.draw.rect(screen, btColor,((515,10),(145, 50)))
                        fontch = pygame.font.SysFont('simHei',18)
                        txt = fontch.render(namestr, True, (0,0,0))
                        screen.blit(txt, (520,25))
                        pygame.display.flip()

    return namestr

def comment_creater2(move,total_score,rhythm):
    #根据分数生成评语
    return evaluation

def print_comment(screen,comment):
    thres=36
    upb=697 #720
    if len(comment)>thres:
        comment1=comment[:thres]
        comment2=comment[thres:]
        fontch = pygame.font.SysFont('simHei',18)
        txt = fontch.render(comment1, True, (0,0,0))
        screen.blit(txt, (30,upb))
        txt = fontch.render(comment2, True, (0,0,0))
        screen.blit(txt, (30+54,upb+23))
    else:
        fontch = pygame.font.SysFont('simHei',18)
        txt = fontch.render(comment, True, (0,0,0))
        screen.blit(txt, (30,upb))
    pygame.display.flip()

def print_posing_info(screen,n):
    fontch = pygame.font.SysFont('simHei',22)
    if not n:
        txt = fontch.render('姿态识别中...', True, (255,0,0))
        screen.blit(txt, (150,84))
    else:
        pygame.draw.rect(screen, bgColor,((150,70),(140, 50)))
        txt = fontch.render('评分已完成', True, (255,0,0))
        screen.blit(txt, (150,84))
    pygame.display.flip()

def create_polar(move,total_score,rhythm_score,name,test_name):

    #通过关节点分数计算动作细节分数

    #如果总分太低则节奏分数没有意义
    if total_score<80:
        rhythm_score=0
    
    tb=pd.DataFrame(np.array([['hands',hands],
                        ['shoulders',shoulder],
                        ['legs',leg],
                        ['gravity center',steady],
                        ['rhythm',rhythm_score],
                        ['key force',core]]))

    print("得分：",total_score)

    move_comment=[]
    for i in move:
        move_comment.append(i[1]/100)

    comment=comment_creater2(move_comment,total_score,rhythm_score)
    print("评语：")
    print(comment)
    comment="评语："+comment

    print("各部位得分：")
    print(tb)


    values = [hands,shoulder,leg,steady,rhythm_score,core]
    feature = ['手部','肩部','下肢','身体重心','节奏','核心力量']
    #feature = ['hands','shoulders','legs','gravity center','rhythm','key force']

    plt.rcParams['font.sans-serif'] = 'SimHei'
    #用于正常显示符号
    plt.rcParams['axes.unicode_minus'] = False

    angles=np.linspace(0, 2*np.pi,len(values), endpoint=False)

    values=np.concatenate((values,[values[0]]))
    angles=np.concatenate((angles,[angles[0]]))

    # 绘图
    fig=plt.figure()
    # 设置为极坐标格式
    ax = fig.add_subplot(111, polar=True)
    # 绘制折线图
    ax.plot(angles, values, 'o-', linewidth=1)
    #ax.plot(angles, values, 'o-', c='b',linewidth=2)


    # 设置图标上的角度划分刻度，为每个数据点处添加标签
    feature = np.concatenate((feature,[feature[0]]))
    ax.set_thetagrids(angles * 180/np.pi, feature)
    
    # 设置雷达图的范围
    ax.set_ylim(0,1)

    # 添加网格线
    ax.grid(True)
    plt.fill(angles,values)

    plt.savefig(rootpath+'scores/'+name+'_'+test_name+'.png')
    return comment