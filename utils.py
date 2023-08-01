import os
import time


def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)

def get_pic_name(ns=''):
    name=ns
    t=time.ctime().split(' ')[3]
    tlist=t.split(':')
    for i in tlist:
        name+='_'+i
    name+='.jpg'

    return name

def get_json_name(ns=''):
    name=ns
    t=time.ctime().split(' ')[3]
    tlist=t.split(':')
    for i in tlist:
        name+='_'+i
    name+='.json'

    return name

def create_path(root,file_name,del_all=True):
    #root后面加/，file_name不加/
    if os.path.exists(root+file_name):
        if del_all:
            del_file(root+file_name)
        return
    else:
        os.mkdir(root+file_name)

def name_in_list(name,namelist):
    for i in namelist:
        if name==str(i):
            return True
    return False


# root1='C:/Users/dengl/Desktop/activity/score_video_ui/origin_jsons/'
# root2='C:/Users/dengl/Desktop/activity/score_video_ui/imitate_jsons/'
# create_path(root1,'1')
# create_path(root2,'1')
# create_path(root2+'1/','1')
# create_path(root2+'1/','2')
# create_path(root2+'1/','3')