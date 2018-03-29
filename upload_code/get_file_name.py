# -*- coding: utf-8 -*-

import os
import argparse
import sys

def get_file_name_list(file_path):
    result=[]
    for file in os.listdir(file_path):
        temp_file=file.split(".jpg")[0]
        result.append(temp_file)
    return result

def get_train_val_list(file_list,val_ratio):
    if float(val_ratio) > 0.5:
        raise Exception("val_ratio is too large, please set it between 0.1 and 0.4")
    train_start=0
    train_end=int(len(file_list)*(1-float(val_ratio)))
    val_start=train_end
    val_end=len(file_list)
    train_list=file_list[train_start:train_end]
    val_list=file_list[val_start:val_end]
    return train_list,val_list

def write_file_list(txt_path,file_list,is_train=True):
    if not os.path.exists(txt_path):
        print("txt_path not exists, so create it")
        os.mkdir(txt_path)
    if len(file_list) == 0:
        raise Exception("length of file_list is zero, please check file_list")
    txt_file=None
    if is_train:
        txt_file=os.path.join(txt_path,"train.txt")
    else:
        txt_file=os.path.join(txt_path,"val.txt")

    f_txt=open(txt_file,'w')
    for i in range(len(file_list)):
        if i != len(file_list)-1:
            f_txt.write(str(file_list[i])+"\n")
        else:
            f_txt.write(str(file_list[i]))
    f_txt.close()

def parse_args():
    parser=argparse.ArgumentParser(description="get file names in a folder")
    parser.add_argument("--img_path",default="~/data/VOCdevkit/VOC2007/JPEGImages",
                        help="where image files exist",type=str)
    parser.add_argument("--txt_path",default="~/data/VOCdevkit/VOC2007/ImageSets",
                        help="where txt files will be stored",type=str)
    parser.add_argument("--val_ratio",default=0.3,
                        help="the ratio of val_set/(train_set+val_set)",type=float)

    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit()

    args=parser.parse_args()
    return args

if __name__=="__main__":
    args=parse_args()
    print("Called with args:")
    print(args)
    train_val_list=get_file_name_list(args.img_path)
    train_list,val_list=get_train_val_list(train_val_list,args.val_ratio)
    write_file_list(args.txt_path,train_list,is_train=True)
    write_file_list(args.txt_path,val_list,is_train=False)




















