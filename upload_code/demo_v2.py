#!/usr/bin/env python

# --------------------------------------------------------
# Tensorflow Faster R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Xinlei Chen, based on code from Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths
from model.config import cfg
from model.test import im_detect
from model.nms_wrapper import nms

from utils.timer import Timer
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os, cv2
import argparse
import xml.dom.minidom

from nets.vgg16 import vgg16
from nets.resnet_v1 import resnetv1



CLASSES = ('__background__',
           'tpi','xb','pepsi','nmc','glc')

NETS = {'vgg16': ('vgg16_faster_rcnn_iter_70000.ckpt',),'res101': ('res101_faster_rcnn_iter_110000.ckpt',)}
DATASETS= {'pascal_voc': ('voc_2007_trainval',),'pascal_voc_0712': ('voc_2007_trainval+voc_2012_trainval',)}

test_img_path="/home/hgobox_wh/proj/tf-faster-rcnn/data/result_img/"
output_xml_path="/home/hgobox_wh/proj/tf-faster-rcnn/data/result_xml/"



def xml_write(img_path,xml_path,img_file,img_shape,contents,with_score=False):
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

    for element in contents:
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
            bndbox_node.appendChild(score_node)

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


def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor='red', linewidth=3.5)
            )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')

    ax.set_title(('{} detections with '
                  'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                  fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.draw()

def print_detection(im_file,im, class_name, dets, img_shape,thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return
    contents=[]
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        cv2.rectangle(im,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,0,255),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        score=("%.3f" % float(score))
        cv2.putText(im,str(class_name)+":"+str(score),(int(bbox[0]),int(bbox[1]-2)),font,0.45,(255,0,0),1)
        print(("{} detections with p({} | box) >= {:.1f}").format(class_name, class_name,thresh))

        element=bbox
        element.extend(score)
        element.extend(class_name)
        contents.append(element)
        element.clear()

    im_file=im_file.split('/')[-1]
    cv2.imwrite(os.path.join(test_img_path,im_file),im)

    xml_write(test_img_path, output_xml_path, im_file,img_shape,contents,with_score=True)


def demo(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(cfg.DATA_DIR, 'demo/test_imgs', image_name)
    if not os.path.exists(im_file):
        print("Please check where test images exist!!!!!\n")
    im = cv2.imread(im_file)
    shape=im.shape

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()
    print('Detection took {:.3f}s for {:d} object proposals'.format(timer.total_time, boxes.shape[0]))

    # Visualize detections for each class
    CONF_THRESH = 0.8
    NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        # vis_detections(im, cls, dets, thresh=CONF_THRESH)
        print_detection(im_file,im,cls,dets,shape,thresh=CONF_THRESH)

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16 res101]',
                        choices=NETS.keys(), default='res101')
    parser.add_argument('--dataset', dest='dataset', help='Trained dataset [pascal_voc pascal_voc_0712]',
                        choices=DATASETS.keys(), default='pascal_voc_0712')
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals
    args = parse_args()

    # model path
    demonet = args.demo_net
    dataset = args.dataset
    tfmodel = os.path.join('output', demonet, DATASETS[dataset][0], 'default',
                              'res101_faster_rcnn_iter_50000.ckpt')


    if not os.path.isfile(tfmodel + '.meta'):
        raise IOError(('{:s} not found.\nDid you download the proper networks from '
                       'our server and place them properly?').format(tfmodel + '.meta'))

    # set config
    tfconfig = tf.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth=True

    # init session
    sess = tf.Session(config=tfconfig)
    # load network
    if demonet == 'vgg16':
        net = vgg16()
    elif demonet == 'res101':
        net = resnetv1(num_layers=101)
    else:
        raise NotImplementedError
    net.create_architecture("TEST", 6,
                          tag='default', anchor_scales=[8, 16, 32])
    saver = tf.train.Saver()
    saver.restore(sess, tfmodel)
    print('Loaded network {:s}'.format(tfmodel))
    im_names=[]
    for temp_file in os.listdir(test_img_path):
        im_names.append(temp_file)

    for im_name in im_names:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Demo for {}/{}'.format(test_img_path,im_name))
        demo(sess, net, im_name)

