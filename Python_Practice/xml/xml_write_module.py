# -*- coding:utf-8 -*-

import xml.dom.minidom
import os


def xml_write(img_path,xml_path,img_file,img_shape,content,with_score=False):
    if not os.path.exists(xml_path):
        os.mkdir(xml_path)

    assert len(img_shape) == 3

    doc=xml.dom.minidom.Document()
    root=doc.createElement("annotations")
    doc.appendChild(root)

    folder_node=doc.createElement("folder")
    folder_node.appendChild(doc.createTextNode("img"))
    filename_node=doc.createElement("filename")
    filename_node.appendChild(doc.createTextNode(str(img_file)))
    path_node=doc.createElement("path")
    path_node.appendChild(doc.createTextNode(str(os.path.join(img_path,img_file))))
    source_node=doc.createElement("source")
    database_node=doc.createElement("database")
    database_node.appendChild(doc.createTextNode("Unknown"))
    source_node.appendChild(database_node)

    size_node=doc.createElement("size")
    width_node=doc.createElement("width")
    width_node.appendChild(doc.createTextNode(str(img_shape[1])))
    height_node=doc.createElement("height")
    height_node.appendChild(doc.createTextNode(str(img_shape[0])))
    depth_node=doc.createElement("depth")
    depth_node.appendChild(doc.createTextNode(str(img_shape[2])))
    size_node.appendChild(width_node)
    size_node.appendChild(height_node)
    size_node.appendChild(depth_node)

    segmented_node=doc.createElement("segmented")
    segmented_node.appendChild(doc.createTextNode("0"))

    root.appendChild(folder_node)
    root.appendChild(filename_node)
    root.appendChild(path_node)
    root.appendChild(source_node)
    root.appendChild(size_node)
    root.appendChild(segmented_node)

    for element in content:
        assert len(element) == 6

        object_node = doc.createElement("object")
        name_node=doc.createElement("name")
        name_node.appendChild(doc.createTextNode(str(element[-1])))
        pose_node=doc.createElement("pose")
        pose_node.appendChild(doc.createTextNode("Unspecified"))
        truncated_node=doc.createElement("truncated")
        truncated_node.appendChild(doc.createTextNode("0"))
        difficult_node=doc.createElement("difficult")
        difficult_node.appendChild(doc.createTextNode("0"))
        bndbox_node=doc.createElement("bndbox")

        xmin_node=doc.createElement("xmin")
        xmin_node.appendChild(doc.createTextNode(str(element[0])))
        ymin_node=doc.createElement("ymin")
        ymin_node.appendChild(doc.createTextNode(str(element[1])))
        xmax_node=doc.createElement("xmax")
        xmax_node.appendChild(doc.createTextNode(str(element[2])))
        ymax_node=doc.createElement("ymax")
        ymax_node.appendChild(doc.createTextNode(str(element[3])))

        bndbox_node.appendChild(xmin_node)
        bndbox_node.appendChild(ymin_node)
        bndbox_node.appendChild(xmax_node)
        bndbox_node.appendChild(ymax_node)

        if with_score:
            score_node=doc.createElement("score")
            score_node.appendChild(doc.createTextNode(str(element[4])))
            object_node.appendChild(score_node)

        object_node.appendChild(name_node)
        object_node.appendChild(pose_node)
        object_node.appendChild(truncated_node)
        object_node.appendChild(difficult_node)
        object_node.appendChild(bndbox_node)

        root.appendChild(object_node)

    xml_file=img_file.split(".jpg")[0]+".xml"
    dst_file=os.path.join(xml_path,xml_file)
    xml_writer=open(dst_file,'w',encoding="utf-8")
    doc.writexml(xml_writer,indent='\t',addindent="    ",newl='\n',encoding="utf-8")


if __name__=="__main__":
    img_path="E:/Work/TestImages/"
    xml_path="E:/Work/TestImages/xml/"
    img_file="test.jpg"
    img_shape=(2048, 1520, 3)
    content=[[123,234,324,445,0.80,"glc"],[1,1,10,10,0.70,"pepsi"]]

    xml_write(img_path,xml_path,img_file,img_shape,content)

