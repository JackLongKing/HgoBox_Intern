# -*- coding: utf-8 -*-
# show ground truth png images of pascal voc with colormap

import os
import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt

def gray2color(gray_array, color_map):
    rows, cols = gray_array.shape
    color_array = np.zeros((rows, cols, 3), np.uint8)

    for i in range(0, rows):
        for j in range(0, cols):
            color_array[i, j] = color_map[gray_array[i, j]]

            # color_image = Image.fromarray(color_array)

    return color_array


def test_gray2color(test_png):
    gray_image = Image.open(test_png).convert("L")

    gray_array = np.array(gray_image)

    plt.figure()
    plt.subplot(211)
    plt.imshow(gray_array, cmap='gray')

    # jet_map = np.loadtxt('E:\\Development\\Thermal\\ColorMaps\\jet_int.txt', dtype=np.int)
    jet_map=labelcolormap(5)
    color_jet = gray2color(gray_array, jet_map)
    plt.subplot(212)
    plt.imshow(color_jet)
    plt.savefig(test_png.split(".png")[0]+"_res"+".png")
    plt.show()

    return

def bitget(byteval, idx):
    return ((byteval & (1 << idx)) != 0)

def labelcolormap(N=256):
    cmap = np.zeros((N, 3))  #N是类别数目
    for i in range(0, N):
        id = i
        r, g, b = 0, 0, 0
        for j in range(0, 8):
            r = np.bitwise_or(r, (bitget(id, 0) << 7-j))
            g = np.bitwise_or(g, (bitget(id, 1) << 7-j))
            b = np.bitwise_or(b, (bitget(id, 2) << 7-j))
            id = (id >> 3)
        cmap[i, 0] = r
        cmap[i, 1] = g
        cmap[i, 2] = b
    cmap = cmap.astype(np.float32) / 255 #获得Cmap的RGB值
    return cmap

os.chdir(r'C:\Users\Administrator\Desktop\test')
path=os.getcwd()
files=os.listdir(path)
labels_path=os.path.join(path,'labels')

for file in files:
    file=os.path.join(path,file)
    test_gray2color(file)


