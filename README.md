# DanceInCloudScoringDemo
A demo for dancing scoring using Openpose from *DanceInCloud*.


## Introduction
This repo provides a framework to use your customized scoring algorithm to do scoring and evaluating to the dancing videos based on standard dancing videos. In addition to dancing, other videos that are rated according to standard movements, such as fitness movements, martial arts, and yoga, can also be rated and evaluated using this framework.

This version supports *video* scoring, including *video choosing mode* and *video recording mode*. You can choose a ready-made video or use the framework to record your dancing moves directly. After uploading the video, the framework will do pose estimation, score regression and remark generation. The score includes dancing move score and rhythm score. The dancing move score includes total score and detail scores for each joint.

## Demo

A website demo using scoring framework.

![img](media/website.gif)

We provide a simple pygame demo in this repo.

![img](media/pygame.gif)

## Usage

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
