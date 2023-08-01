import numpy as np
from math import acos
from dtw import dtw
from scipy.optimize import least_squares

from json_funcs import *


def cal_score_by_dtw_video(kpd1, kpd2, invalid_list):
    #通过角度差进行分数回归预测，回归模型参数可以通过舞蹈视频数据和评分得出
    
    return score_avg2, rhythm_avg

def main_2(ns,origin_json_path,imitate_json_path): #分数计算函数，返回动作分数和节奏分数
    # 角度关键点集合
    keypoint_set = np.array([
        [3, 2, 4],  # 右手
        [6, 7, 5],  # 左手
        [2, 1, 3],  # 右肩
        [5, 6, 1],  # 左肩
        [1, 0, 8],  # 头与躯干
        [1, 2, 8],  # 右肩与躯干
        [1, 5, 8],  # 左肩与躯干
        [8, 9, 1],  # 躯干与右髋
        [8, 12, 1],  # 躯干与左髋
        [9, 8, 10],  # 右腿与髋
        [12, 8, 13],  # 左腿与髋
        [10, 9, 11],  # 右脚
        [13, 12, 14],  # 左脚
        [11, 10, 22],  # 右脚踝
        [14, 13, 19],  # 左脚踝
    ], dtype=int)

    #关键点集合，[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 19 22]
    key_point_list = np.unique(keypoint_set)

    # 无效帧列表
    invalid_frame1 = {'no_people_frame': [],
                      'low_prob_frame': [],
                      'reverse_frame': [],
                      }

    invalid_frame2 = {'no_people_frame': [],
                      'low_prob_frame': [],
                      'reverse_frame': [],
                      }

    # 读取json文件  lj:三维数组，帧数*关键点数*3(横坐标、纵坐标、置信度)   lr:一维数组，每一帧的flag(1正面 2反面 0无效)
    lj2,lr2 = read_json_imitate_video(imitate_json_path,key_point_list,invalid_frame2)
    lj1,lr1 = read_json_origin_video(origin_json_path,key_point_list,invalid_frame1)

    # 算分
    scores,rhythm_score = cal_score_by_dtw_video()

    return scores,rhythm_score

def score_print(ns,origin_json_path,imitate_json_path):
    kpscores,rhythm_score=main_2(ns,origin_json_path,imitate_json_path)
    kpscores=kpscores.reshape(1,-1)

    #分数整合，包括总分，各项细节分，节奏分

    return scoresum,name_score,rhythm_score
