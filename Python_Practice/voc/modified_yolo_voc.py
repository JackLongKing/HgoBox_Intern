# -*- coding:utf-8 -*-
# darknet convert xml to txt format

import xml.etree.ElementTree as ET
import os
import numpy as np

classes = ["tpi", "xb", "pepsi", "nmc", "glc"]
val_ratio=0.2
jpg_path="/home/gulong/data/darknet/train_img"
xml_path="/home/gulong/data/darknet/train_xml"
txt_path="/home/gulong/data/darknet/train_txt"
list_path="/home/gulong/data/darknet"

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def get_train_val_list(file_list,val_ratio):
    np.random.shuffle(file_list)
    train_start = 0
    train_end = int(len(file_list) * (1 - float(val_ratio)))
    val_start = train_end
    val_end = len(file_list)
    train_list = file_list[train_start:train_end]
    val_list = file_list[val_start:val_end]
    return train_list, val_list

def convert_annotation(xml_path, txt_path,jpg_path,list_path,val_raio):
    print("Start converting: ")
    if not os.path.exists(xml_path) or not os.path.exists(jpg_path):
        raise IOError("XML_PATH or JPG_PATH not exists, please check it!")
    if not os.path.exists(txt_path):
        os.makedirs(txt_path)

    all_jpg_files=[]
    for tmpfile in os.listdir(xml_path):
        xmlfile=os.path.join(xml_path,tmpfile)
        txtfile=tmpfile.split(".xml")[0]+".txt"
        txtfile=os.path.join(txt_path,txtfile)
        jpgfile=tmpfile.split(".xml")[0]+".jpg"
        jpgfile=os.path.join(jpg_path,jpgfile)
        all_jpg_files.append(jpgfile)
        in_file=open(xmlfile)
        out_file=open(txtfile,"w")
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        in_file.close()
        out_file.close()
    train_list,val_list=get_train_val_list(all_jpg_files,val_raio)
    list_file=open(os.path.join(list_path,"train.txt"),"w")
    for train_jpg in train_list:
        list_file.write(train_jpg+"\n")
    list_file.close()
    list_file=open(os.path.join(list_path,"val.txt"),"w")
    for val_jpg in val_list:
        list_file.write(val_jpg+"\n")
    list_file.close()
    print("Converting Ended! ")

convert_annotation(xml_path,txt_path,jpg_path,list_path,val_ratio)
