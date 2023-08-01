import os
import cv2
from datetime import datetime

def video_capture(origin_name,save_path='C:/Users/dengl/Desktop/activity/imitation_video_ui/imitate_videos/',duration=5,WIDTH=1280,HEIGHT=720,FPS=24,preview=False):
    imitate_name=origin_name+'.mp4'
    FILENAME = save_path+imitate_name

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

def openposedemo_video_origin(input_video,output_video,output_json,openpose_path,face=False,hand=False): #生成识别后的视频
    cwd=os.getcwd()
    os.chdir(openpose_path)
    command='OpenPoseDemo --video '+input_video+' --write_video '+output_video+' --write_json '+output_json
    if face:
        command+=' --face'
    if hand:
        command+=' --hand'
    os.system(command)
    os.chdir(cwd)

def main(namelist=[],num=1,duration=3,camera=False):
    openpose_path='openpose/bin/'
    if camera:
        if len(namelist)==0:
            for i in range(1,num+1):
                video_capture(str(i),save_path='C:/Users/dengl/Desktop/activity/score_video_ui/origin_videos/',duration=duration)
        else:
            for name in namelist:
                video_capture(name,save_path='C:/Users/dengl/Desktop/activity/score_video_ui/origin_videos/',duration=duration)
    input_path='C:/Users/dengl/Desktop/activity/score_video_ui/origin_videos/'
    output_path='C:/Users/dengl/Desktop/activity/score_video_ui/origin_rendered_videos/'
    json_path='C:/Users/dengl/Desktop/activity/score_video_ui/origin_jsons/'
    if len(namelist)==0:
        names=os.listdir(input_path)
    else:
        names=namelist
    for name in names:
        input_video=input_path+name+'.mp4'
        output_video=output_path+name+'.avi'
        output_json=json_path+name+'/'
        openposedemo_video_origin(input_video,output_video,output_json,openpose_path)

main(namelist=['2'],camera=False)