# -*- coding:utf-8 -*-
import os

myfile="0425152730_0_40.jpg"
# print(myfile.split("_"))
content=myfile.split("_")
print(len(content))

myFile="E:\\Work\\TestImages\\xml\\test.xml"
print(os.path.basename(myFile))
print(os.path.splitext(myFile)[1])




