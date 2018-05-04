# -*- coding:utf-8 -*-

import os
import xml
from xml.dom import minidom

def modify_xml(xml_file):
    dom=xml.dom.minidom.parse(xml_file)
    root=dom.documentElement
    object_nodes=root.getElementsByTagName("object")
    # print(len(object_nodes))
    for i in range(len(object_nodes)):
        object_node = object_nodes[i]
        name_node = object_node.getElementsByTagName("name")[0]
        name_text = name_node.childNodes[0]
        if name_text.data == "cpi":
            # print(name_text.data)
            name_text.data = "tpi"

    with open(xml_file,'w') as fh:
        dom.writexml(fh)

def get_file_name_list(xml_path):
    all_files=[]
    for root_dir,dirs,files in os.walk(xml_path):
        for tmp_file in files:
            all_files.append(os.path.join(root_dir,tmp_file))
    # print(len(all_files))
    return all_files

def modify(all_files):
    for i in range(len(all_files)):
        if os.path.splitext(all_files[i])[1] ==".xml":
            modify_xml(all_files[i])

# def test():
#     # xml_file="E:\\Work\\PyCharm\\Python_Practice\\xml\\test.xml"
#     # modify_xml(xml_file)
#     xml_path="E:\\Work\\PyCharm\\Python_Practice"
#     get_file_name_list(xml_path)
# test()

xml_path=""
all_files=get_file_name_list(xml_path)
modify(all_files)
















