# -*- coding: utf-8 -*-

#import modules
import cv2
import os
import os.path
import json
from statistics import mean


# In[213]:


#define valuables & lists
ImgPerSeg = 1
annotation = '../annotations/youcookii_annotations_trainval.json'
video_names = []
segments = {}
subsets = {'training':{},'validation':{},'testing':{}}
segments_num = {}


# In[214]:

# read annotation file

# load json file
with open(annotation) as data_file:
    data = json.load(data_file)

# save names of videos
for i in data['database'].keys():
    video_names.append(i)

# save dulation of annoted segments of each videos

for name in video_names:
    subset = data['database'][name]['subset']
    recipe_type = data['database'][name]["recipe_type"]
    annotations = data['database'][name]['annotations']
    try:
        subsets[subset][recipe_type][name] = []
    except:
        subsets[subset][recipe_type]= {}
        subsets[subset][recipe_type][name] = []

    for i in annotations:
        id = i['id']
        subsets[subset][recipe_type][name].append(i['segment'])
        subsets[subset][recipe_type][name][-1] = round(mean(subsets[subset][recipe_type][name][-1]))

# In[215]:


#define valuables & lists
count = 0
sec = 0
sec_count = 0

# In[216]:


for subset, value in subsets.items():
    for recipe_type, value2 in value.items():
        for name,segment in value2.items():
            img_path = os.path.join("../images",subset,recipe_type,name)
            video_path =  os.path.join("../raw_videos",subset,recipe_type)
            if not os.path.isdir(img_path):
                os.makedirs(img_path)
            video = name+'.mkv'
            if not os.path.isfile(video_path +"/" + video):
                video = name+'.mp4'
            cap = cv2.VideoCapture(video_path +"/"+  video)
            video_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            video_fps = cap.get(cv2.CAP_PROP_FPS)

            img_num = 0
            segment_num = 0
            while True:
                ret, frame = cap.read()
                if ret == True:
                    count += 1
                    if count % round(video_fps) == 0:
                        sec += 1
                        sec_count = 0

                    if sec_count== 0:
                        for i in range(len(segment)):
                            if sec == segment[i]:
                                if segment_num != i:
                                    img_num = 0
                                print(sec)

                                segment_num = i
                                if not os.path.isfile(img_path + "/" + str(segment_num).zfill(2) +"-" + str(img_num).zfill(3)+ '.jpg'):
                                    cv2.imwrite(img_path + "/"+ str(segment_num).zfill(2) +"-" + str(img_num).zfill(3)+ '.jpg', frame)
                                img_num += 1
                    if img_num >= ImgPerSeg:
                            sec_count += 1



                else:
                    count = 0
                    sec = 0
                    break

            with open("logs/get_images_per_segment.log", "a") as f:
                print(subset,recipe_type,name,video_frame,round(video_fps),segment_num + 1,"segments -->saved",file=f)
