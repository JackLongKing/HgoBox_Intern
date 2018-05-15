# -*- coding:utf-8 -*-

import argparse
import json
import matplotlib.pyplot as plt

from labelme import utils


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('json_file')
    # args = parser.parse_args()
    #
    # json_file = args.json_file
    # json_file=r"C:\Users\Administrator\Desktop\windows_v1.5.1\data\WIN_20180504_10_05_03_Pro.json"
    json_file=r"C:\Users\Administrator\Desktop\windows_v1.5.1\data\img00000001.json"

    data = json.load(open(json_file))

    img = utils.img_b64_to_array(data['imageData'])
    lbl, lbl_names = utils.labelme_shapes_to_label(img.shape, data['shapes'])

    lbl_viz = utils.draw_label(lbl, img, lbl_names)

    plt.imshow(lbl_viz)
    plt.show()


if __name__ == '__main__':
    main()




























