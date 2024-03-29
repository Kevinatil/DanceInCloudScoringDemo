# Dance In Cloud Scoring Demo
A demo for dancing scoring using Openpose from *DanceInCloud*.


Noted that this repo is just a framework without detailed scoring process. If you want to calculate scores using our scoring process and regression weights, please turn to [MoveImitatingGame-DanceInCloud](https://github.com/Kevinatil/MoveImitatingGame-DanceInCloud/) where we provide a full scoring process with scoring functions obfuscated by `pyarmor`.

## Introduction
This repo provides a framework to use your customized scoring algorithm to do scoring and evaluating to the dancing videos based on standard dancing videos. In addition to dancing, other videos that are rated according to standard movements, such as fitness movements, martial arts, and yoga, can also be rated and evaluated using this framework.

This version supports *video* scoring, including *video choosing mode* and *video recording mode*. You can choose a ready-made video or use the framework to record your dancing movements directly. After uploading the video, the framework will do pose estimation, score regression and remark generation. The score includes dancing movement score and rhythm score. The dancing movement score includes total score and detail scores for each joint.

## Environment

The scoring process is based on [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose). Please configure the OpenPose environment before running this framework.

```bash
# After configuring OpenPose, run command to install packages
pip install -r requirements.txt
```

## Demo

The *Dance In Cloud* online dance evaluation platform.

https://github.com/Kevinatil/DanceInCloudScoringDemo/assets/64370697/7b8f4acc-b564-4345-8bb2-8383c9b3a740

We provide a simple pygame demo in this repo using the same scoring process as the online platform. We removed the regression weights and scoring details because of the commercial usage. You can define your own evaluation function based on your actual usage.

![img](https://github.com/Kevinatil/DanceInCloudScoringDemo/blob/main/media/pygame.gif)

## Usage

Noted that this repo is just a pygame framework without detailed scoring process. If you want to get real scores from our process, please turn to [MoveImitatingGame-DanceInCloud](https://github.com/Kevinatil/MoveImitatingGame-DanceInCloud/) where we provide a full scoring process with scoring functions obfuscated by `pyarmor`.

(1) Use ready-made video to score

1. Put the target(standard) video into `origin_videos` folder;
 
2. Open *origin.py*, change `namelist` in `main` into the name of the target video(without .mp4);
 
3. Noted that `camera` in `main` should be set to *False*, otherwise the videos under the target folder could be deleted;
 
4. Run *origin.py*, and the rendered video and extracted json files will be generated;
 
5. (optional) put a thumbnail of the standard video into `origin_pics` folder;
 
6. Run *imitate.py* after changing the work directory based on your environment;
 
7. The scoring process can be restarted by clicking input box.

(2) Record the standard video

1. Open *origin.py*, change `namelist` into the name of the video to be recording, or set `namelist` as empty to use default name;
 
2. Set the `camera` as *True* in *origin.py*;
 
3. Run *origin.py* to do video recording, and the rendered video and extracted json files will be generated;
 
4. (optional) put a thumbnail of the standard video into `origin_pics` folder;
 
5. Run *imitate.py* after changing the work directory based on your environment;
 
6. The scoring process can be restarted by clicking input box.


## Acknowledgement

We thank Shanghai Film Art Academy for the standard dancing videos, test dancing videos and official scores for model training. 

We thank Shanghai Film Art Academy and Beijing Dance Academy for the testing and valuable suggestions on our website.
