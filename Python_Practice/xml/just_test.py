# -*- coding:utf-8 -*-

# ===========================================================================================
# import os
# myfile="0425152730_0_40.jpg"
# # print(myfile.split("_"))
# content=myfile.split("_")
# print(len(content))
#
# myFile="E:\\Work\\TestImages\\xml\\test.xml"
# print(os.path.basename(myFile))
# print(os.path.splitext(myFile)[1])
#
#
# content=[[1,2,3,4],[1,3,4,5]]
# all_contents=content
# all_contents.extend(content)
# print(all_contents)
# print(len(all_contents))

# ===========================================================================================
import cv2

img_file=r"E:\Work\TestImages\res_test_0.jpg"
img=cv2.imread(img_file)
print(img.shape)

image_format=["jpg","png","JPG","JPEG",'tif',"gif"]
if "png" in image_format:
    print("True")

im_file="/home/file/img_2000000.jpg"
print(im_file.split("/")[-1].split(".")[-1])
# if im_file.splitext()[1] in image_format:
#     print("True")




















