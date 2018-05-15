# -*- coding:utf-8 -*-

import os

file_path="/home/gulong/project/deeplab/models/research/deeplab/datasets/pascal_voc_seg/VOCdevkit/VOC2012/SegmentationClass"
# tmp_path=r"C:\Users\Administrator\Desktop\test_1"
path=file_path

print("Start:")
for file in os.listdir(path):
    all_splits=file.split("__")
    # print(all_splits)
    new_file=all_splits[0]+"_"+all_splits[1]
    src_file=os.path.join(path,file)
    dst_file=os.path.join(path,new_file)
    os.rename(src_file,dst_file)
print("Done!")













