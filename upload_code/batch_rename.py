# -*- coding:utf-8 -*-

import os

img_path="E:\\Work\\Data\\temp\\image"
label_path="E:\\Work\\Data\\temp\\label"
time="180409_"
category="low_"
state="mixture_" # stand, down, mixture

print("rename start: \n")
for temp_file in os.listdir(img_path):
    dst_file=time+category+state+temp_file
    os.rename(os.path.join(img_path,temp_file),os.path.join(img_path,dst_file))

for temp_file in os.listdir(label_path):
    dst_file=time+category+state+temp_file
    os.rename(os.path.join(label_path,temp_file),os.path.join(label_path,dst_file))

print("rename end! \n")
























