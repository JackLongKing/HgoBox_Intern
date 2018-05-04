# -*- coding:utf-8  -*-

import os
import shutil
import xml
from xml.dom import minidom

def copy_file(ori_path,dst_path,dst_list):
    print("Copy file start: ")
    for file in os.listdir(ori_path):
        ori_file=os.path.join(ori_path,file)
        content=file.split("_")
        # print(content)
        for i in range(len(dst_list)):
            dst_file=os.path.join(dst_path,str(content[0])+"_"+str(content[1])+"_"+str(dst_list[i])+".xml")
            # print(dst_file)
            shutil.copyfile(ori_file,dst_file)

    print("Copy file end!")

def modify_xml(dst_path):
    print("Modify start: ")
    for xml_file in os.listdir(dst_path):
        # print(xml_file)
        dom=xml.dom.minidom.parse(os.path.join(dst_path,xml_file))
        root=dom.documentElement
        # print(root.nodeName)
        filename_node=root.getElementsByTagName("filename")[0]
        filename_text=filename_node.childNodes[0]
        filename_text.data=str(xml_file.split(".xml")[0])+".jpg"

        path_node=root.getElementsByTagName("path")[0]
        path_text=path_node.childNodes[0]
        # print(os.path.basename(path_text.data))
        path_text.data=path_text.data.split(os.path.basename(path_text.data))[0] + filename_text.data

        with open(os.path.join(dst_path, xml_file), 'w') as fh:
            dom.writexml(fh)
    print("Modify end!")





ori_path="E:\\Work\\Data\\labeled_data\\20180425\\ori_xml"
dst_path="E:\\Work\\Data\\labeled_data\\20180425\\dst_xml"
dst_list=['040', '050', '060', '070', '080', '090', '100', '110', '120', '130', '140', '150', '160', '170', '180', '190', '200', '210', '220', '230', '240', '250', '260', '270', '280']
# dst_list=[]
# for i in range(40,290,10):
#     dst_list.append(("%3d" % i))
# print(dst_list)
copy_file(ori_path,dst_path,dst_list)
modify_xml(dst_path)

















