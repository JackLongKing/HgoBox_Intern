# -*- coding:utf-8 -*-

import os
import shutil
import numpy as np

cur_dir="/home/hgobox_wh/proj/tf-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages"
dst_dir="/home/hgobox_wh/proj/tf-faster-rcnn/data/demo/test_imgs"
test_txt="/home/hgobox_wh/proj/tf-faster-rcnn/data/VOCdevkit2007/VOC2007/ImageSets/Main/test.txt"
num_test_imgs=20

def remove_imgs(test_txt):
    dst_file_list=[]
    f_txt=open(test_txt,'r')
    all_files=f_txt.readlines()
    for i in range(num_test_imgs):
        rand_num=np.random.randint(0,len(all_files))
        dst_file_list.append(all_files[rand_num].strip()+".jpg")
    print("remove start:\n")
    for i in range(len(dst_file_list)):
        src=os.path.join(cur_dir,dst_file_list[i])
        dst=os.path.join(dst_dir,dst_file_list[i])
        shutil.move(src,dst)
    print("remove end!\n")

if __name__=="__main__":
    remove_imgs(test_txt=test_txt)










