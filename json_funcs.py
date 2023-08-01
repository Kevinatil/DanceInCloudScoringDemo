import numpy as np
import json
import os

def read_json_imitate_video(js_pa, kp_list, invalid):
    json_names = os.listdir(js_pa)

    # 总共将读取的帧数
    frame_count = len(json_names)
    print('read from', frame_count, 'frames')

    # 无人帧和低概率帧列表
    no_people_frame_list = []
    low_prob_frame_list = []
    prob_sum = []

    start_frame=0
    end_frame=frame_count-1

    list_json = np.zeros([frame_count, 25, 3], dtype=float)
    lr_flag = np.zeros(frame_count, dtype=int)  # 正面1, 反面2, 无效0

    # 遍历读取范围内的每一个json文件
    for i in range(start_frame, end_frame + 1):
        jname=json_names[i]
        js_name = js_pa + jname
        with open(js_name) as fp:
            json_data = json.load(fp)
            if len(json_data["people"]) == 0:
                # 没有检测到人，写0
                print('no people found, frame', jname)
                kp_data_org = np.zeros(75)
                no_people_frame_list.append(i)
                lr_flag[i - start_frame] = 0
            else:
                # 取概率最大的人（openpose会按概率自动排序，因此取第0号人）
                kp_data_org = np.array(json_data["people"][0]["pose_keypoints_2d"])
                # 根据关节2和关节5的位置（数组的[6]和[15]）判断正反面
                if kp_data_org[6] < kp_data_org[15]:
                    lr_flag[i - start_frame] = 1
                else:
                    lr_flag[i - start_frame] = 2
            kp_data = kp_data_org.reshape(25, 3)
            prob_sum.append(sum(kp_data[kp_list, 2]))#将该帧所有使用到的关节点的置信度相加，为了计算所有帧的平均值以筛选低置信度帧
        list_json[i, ::] = kp_data
    scale=0.95

    prob_sum_threshold = sum(prob_sum) / (frame_count - len(no_people_frame_list)) * scale#低置信度帧阈值

    #筛选低置信度帧
    for i in range(0, frame_count):
        if 0 < prob_sum[i] < prob_sum_threshold:
            low_prob_frame_list.append(i)

    print('low prob', len(low_prob_frame_list), 'frame(s).')
    print('low prob frames: ', low_prob_frame_list)
    print('no people', len(no_people_frame_list), 'frame(s).')
    print('no people frames: ', no_people_frame_list)
    invalid['no_people_frame'] = no_people_frame_list
    invalid['low_prob_frame'] = low_prob_frame_list

    return list_json, lr_flag #list_json:三维数组，帧数*关节点数(25)*3(横坐标、纵坐标、置信度)   lr_flag:一维数组，每一帧的flag(1正面 2反面 0无效)


def read_json_imitate(js_pa):
    json_names = os.listdir(js_pa)

    # 总共将读取的帧数
    frame_count = len(json_names)
    print('read from', frame_count, 'frames')

    list_json = np.zeros([frame_count, 25, 3], dtype=float)

    # 遍历读取范围内的每一个json文件
    for i in range(len(json_names)):
        jname=json_names[i]
        js_name = js_pa + jname
        with open(js_name) as fp:
            json_data = json.load(fp)
            if len(json_data["people"]) == 0:
                # 没有检测到人，写0
                print('no people found, frame', jname)
                kp_data_org = np.zeros(75)
            else:
                # 取概率最大的人（openpose会按概率自动排序，因此取第0号人）
                kp_data_org = np.array(json_data["people"][0]["pose_keypoints_2d"])
            kp_data = kp_data_org.reshape(25, 3)
            
        list_json[i, ::] = kp_data

    return list_json,frame_count #list_json:三维数组，帧数*关节点数(25)*3(横坐标、纵坐标、置信度)   lr_flag:一维数组，每一帧的flag(1正面 2反面 0无效)

def read_json_origin_video(js_pa, kp_list, invalid):
    json_names = os.listdir(js_pa)

    # 总共将读取的帧数
    frame_count = len(json_names)
    print('read from', frame_count, 'frames')

    # 无人帧和低概率帧列表
    no_people_frame_list = []

    start_frame=0
    end_frame=frame_count-1

    list_json = np.zeros([frame_count, 25, 3], dtype=float)
    lr_flag = np.zeros(frame_count, dtype=int)  # 正面1, 反面2, 无效0

    # 遍历读取范围内的每一个json文件
    for i in range(start_frame, end_frame + 1):
        jname=json_names[i]
        js_name = js_pa + jname
        with open(js_name) as fp:
            json_data = json.load(fp)
            if len(json_data["people"]) == 0:
                # 没有检测到人，写0
                print('no people found, frame', jname)
                kp_data_org = np.zeros(75)
                no_people_frame_list.append(i)
                lr_flag[i - start_frame] = 0
            else:
                # 取概率最大的人（openpose会按概率自动排序，因此取第0号人）
                kp_data_org = np.array(json_data["people"][0]["pose_keypoints_2d"])
                # 根据关节2和关节5的位置（数组的[6]和[15]）判断正反面
                if kp_data_org[6] < kp_data_org[15]:
                    lr_flag[i - start_frame] = 1
                else:
                    lr_flag[i - start_frame] = 2
            kp_data = kp_data_org.reshape(25, 3)
        list_json[i, ::] = kp_data

    print('no people', len(no_people_frame_list), 'frame(s).')
    print('no people frames: ', no_people_frame_list)
    invalid['no_people_frame'] = no_people_frame_list

    return list_json, lr_flag #list_json:三维数组，帧数*关节点数(25)*3(横坐标、纵坐标、置信度)   lr_flag:一维数组，每一帧的flag(1正面 2反面 0无效)


def read_json_origin(ns,js_pa,frame_count):
    json_name = ns+'_keypoints.json'

    #frame_count = len(os.listdir('C:\\Users\\dengl\\Desktop\\activity\\imitation\\imitate_jsons\\'))

    list_json = np.zeros([frame_count, 25, 3], dtype=float)

    # 遍历读取范围内的每一个json文件
    
    js_name = js_pa + json_name
    with open(js_name) as fp:
        json_data = json.load(fp)
        # 取概率最大的人（openpose会按概率自动排序，因此取第0号人）
        kp_data_org = np.array(json_data["people"][0]["pose_keypoints_2d"])
        kp_data = kp_data_org.reshape(25, 3)
    
    for i in range(frame_count):
        list_json[i, ::] = kp_data

    return list_json #list_json:三维数组，帧数*关节点数(25)*3(横坐标、纵坐标、置信度)   lr_flag:一维数组，每一帧的flag(1正面 2反面 0无效)
