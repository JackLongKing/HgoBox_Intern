# -*- coding:utf-8 -*-

import cv2

img=cv2.imread("E:\\Work\\TestImages\\res_test_0.jpg")
print(img.shape)

myList=[1,2,3,4]
myList.extend([5])
print(myList)